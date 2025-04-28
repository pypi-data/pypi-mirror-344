import math
import click
from typing import List, Dict
from click.core import ParameterSource

# ── Parameter calculators ──────────────────────────────────────────────────────

def calculate_conv_params(kernel: int, in_ch: int, out_ch: int) -> int:
    return kernel * kernel * in_ch * out_ch + out_ch

def calculate_rnn_params(input_size: int, hidden_size: int) -> int:
    return input_size * hidden_size + hidden_size * hidden_size + hidden_size

def calculate_gru_params(input_size: int, hidden_size: int) -> int:
    return 3 * calculate_rnn_params(input_size, hidden_size)

def calculate_lstm_params(input_size: int, hidden_size: int) -> int:
    return 4 * calculate_rnn_params(input_size, hidden_size)

# ── Argument list parsing ─────────────────────────────────────────────────────

def parse_arg_list(arg: str, num_layers: int, default: int) -> List[int]:
    """
    Turn a comma- or space-separated string of ints into a list of length `num_layers`.
    - If arg is None or empty: returns [default] * num_layers
    - If too short: extends by repeating the last provided value
    - If too long: truncates
    """
    if not arg:
        return [default] * num_layers
    # split on commas or whitespace
    parts = [p for token in arg.split(',') for p in token.strip().split()]
    vals = [int(x) for x in parts]
    # extend or truncate
    if len(vals) < num_layers:
        vals.extend([vals[-1]] * (num_layers - len(vals)))
    return vals[:num_layers]

# ── Encoder / Decoder builders ────────────────────────────────────────────────

def build_encoder(
    in_chs: List[int],
    out_chs: List[int],
    kernels: List[int],
    strides: List[int],
    pads: List[int],
) -> List[Dict]:
    return [
        {
            "layer": i+1,
            "type": "Conv2d",
            "in_channels": in_chs[i],
            "out_channels": out_chs[i],
            "kernel_size": kernels[i],
            "stride": strides[i],
            "padding": pads[i],
            "params": calculate_conv_params(kernels[i], in_chs[i], out_chs[i]),
        }
        for i in range(len(in_chs))
    ]

def build_decoder(
    in_chs: List[int],
    out_chs: List[int],
    kernels: List[int],
    strides: List[int],
    pads: List[int],
) -> List[Dict]:
    rev_ins   = out_chs[::-1]
    rev_outs  = in_chs[::-1]
    rev_k     = kernels[::-1]
    rev_s     = strides[::-1]
    rev_p     = pads[::-1]
    return [
        {
            "layer": i+1,
            "type": "ConvTranspose2d",
            "in_channels": rev_ins[i],
            "out_channels": rev_outs[i],
            "kernel_size": rev_k[i],
            "stride": rev_s[i],
            "padding": rev_p[i],
            "params": calculate_conv_params(rev_k[i], rev_ins[i], rev_outs[i]),
        }
        for i in range(len(rev_ins))
    ]

def print_block(block: List[Dict], name: str) -> None:
    click.echo(f"\n{name}:")
    for L in block:
        click.echo(
            f"  Layer {L['layer']} ─ {L['type']} "
            f"(in={L['in_channels']}, out={L['out_channels']}, "
            f"k={L['kernel_size']}, s={L['stride']}, p={L['padding']}) "
            f"→ {L['params']} params"
        )

# ── CLI Definition ────────────────────────────────────────────────────────────

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--model",
    type=click.Choice(["cnn", "rnn", "gru", "lstm"], case_sensitive=False),
    default="cnn",
    show_default=True,
    help="Type of network to compute parameters for.",
)
@click.option("-n", "--num-layers",    type=int,    default=3,   show_default=True,
              help="Number of layers (CNN or recurrent stack).")
@click.option("--stride",              type=int,    default=1,   show_default=True,
              help="Global default stride for CNN layers.")
@click.option("--kernel-size",         type=int,    default=3,   show_default=True,
              help="Global default kernel size for CNN layers.")
@click.option("--padding",             type=int,    default=1,   show_default=True,
              help="Global default padding for CNN layers.")
@click.option("--in-channels",         type=int,    default=3,   show_default=True,
              help="CNN: input channels (first layer); RNN: input size.")
@click.option("--out-channels",        type=int,    default=64,  show_default=True,
              help="CNN: uniform output channels if set; RNN: hidden size.")
@click.option("--strides",             type=str,    default=None,
              help="Comma/space-separated per-layer strides, e.g. '1 2 3'. Use '0' to fall back to global.")
@click.option("--kernel-sizes",        type=str,    default=None,
              help="Comma/space-separated per-layer kernel sizes, e.g. '3,5,3'. Use '0' to fall back to global.")
@click.option("--paddings",            type=str,    default=None,
              help="Comma/space-separated per-layer paddings, e.g. '1 0 1'. '0' is valid no-padding.")
@click.option("--input-height",        type=int,    default=32,  show_default=True,
              help="CNN: height of the input feature map.")
@click.option("--input-width",         type=int,    default=32,  show_default=True,
              help="CNN: width of the input feature map.")
def main(
    model, num_layers, stride, kernel_size, padding,
    in_channels, out_channels, strides, kernel_sizes, paddings,
    input_height, input_width
):
    """
    Calculate parameter counts for CNN encoder/decoder or RNN/GRU/LSTM stacks,
    with per-layer overrides for strides, kernels, and paddings.
    """
    if model.lower() == "cnn":
        # ── Parse per-layer lists ────────────────────────
        S = parse_arg_list(strides,      num_layers, stride)
        K = parse_arg_list(kernel_sizes, num_layers, kernel_size)
        P = parse_arg_list(paddings,     num_layers, padding)

        # ── Treat '0' in strides/kernels as "use global default" ──
        S = [s if s > 0 else stride      for s in S]
        K = [k if k > 0 else kernel_size for k in K]
        # (P may legitimately be 0 → no padding; keep as-is)

        # ── Decide output channels per layer ──────────────
        ctx     = click.get_current_context()
        out_src = ctx.get_parameter_source("out_channels")
        if out_src == ParameterSource.DEFAULT:
            # auto-double if user DIDN'T set --out-channels
            EC_out = [in_channels * (2 ** (i+1)) for i in range(num_layers)]
        else:
            # uniform out_channels provided
            EC_out = [out_channels] * num_layers
        EC_in  = [in_channels] + EC_out[:-1]

        # ── Basic channel validation ───────────────────────
        if any(ch <= 0 for ch in EC_in + EC_out):
            raise click.BadParameter(f"All channels must be >0; got in={EC_in}, out={EC_out}")

        # ── Validate spatial dims through encoder ──────────
        h, w = input_height, input_width
        for i, (ki, si, pi) in enumerate(zip(K, S, P), start=1):
            nh = math.floor((h + 2*pi - ki) / si) + 1
            nw = math.floor((w + 2*pi - ki) / si) + 1
            if nh < 1 or nw < 1:
                raise click.BadParameter(
                    f"Layer {i} spatial invalid: out={nh}×{nw} from in={h}×{w}"
                )
            h, w = nh, nw

        enc = build_encoder(EC_in, EC_out, K, S, P)

        # ── Validate spatial dims through decoder ──────────
        for i, (ki, si, pi) in enumerate(zip(K[::-1], S[::-1], P[::-1]), start=1):
            nh = (h - 1)*si - 2*pi + ki
            nw = (w - 1)*si - 2*pi + ki
            if nh < 1 or nw < 1:
                raise click.BadParameter(
                    f"Decoder layer {i} invalid: out={nh}×{nw} from in={h}×{w}"
                )
            h, w = nh, nw

        dec = build_decoder(EC_in, EC_out, K, S, P)
        print_block(enc, "Encoder Configuration")
        print_block(dec, "Decoder Configuration")

    else:
        # ── Recurrent modes ───────────────────────────────
        if in_channels <= 0 or out_channels <= 0:
            raise click.BadParameter("--in-channels and --out-channels must be >0")

        results = []
        for idx in range(1, num_layers+1):
            if model.lower() == "rnn":
                p = calculate_rnn_params(in_channels, out_channels); name="RNN"
            elif model.lower() == "gru":
                p = calculate_gru_params(in_channels, out_channels); name="GRU"
            else:
                p = calculate_lstm_params(in_channels, out_channels); name="LSTM"
            results.append((idx, name, in_channels, out_channels, p))
            in_channels = out_channels

        click.echo(f"\n{name} stack ({num_layers} layers):")
        for idx, nm, ic, hc, p in results:
            click.echo(f"  Layer {idx} ─ {nm} (in={ic}, hid={hc}) → {p} params")


if __name__ == "__main__":
    main()
