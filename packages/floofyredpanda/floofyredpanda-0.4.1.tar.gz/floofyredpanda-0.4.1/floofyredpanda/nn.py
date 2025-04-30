import os
import torch
from pickle import UnpicklingError

# optional WAV support
try:
    import soundfile as sf
except ImportError:
    sf = None

# registry for output converters
_output_converters = {
    'int':    lambda t: int(t.item()),
    'float':  lambda t: float(t.item()),
    'str':    lambda t: t.cpu().numpy().tolist() if t.numel() > 1 else str(t.item()),
    'binary': lambda t: t.cpu().numpy().tobytes(),
}

def register_output_converter(name, fn):
    """
    register a custom output converter under `name`
    fn: torch.Tensor -> any
    """
    _output_converters[name] = fn

def get_device(preferred=None):
    """
    decide on CPU vs CUDA, unless caller insists on `preferred`
    """
    if preferred is not None:
        return preferred
    return "cuda" if torch.cuda.is_available() else "cpu"

def load_model_with_fallback(path):
    """
    load a .pt model safely, with fallbacks for unpickling issues
    """
    # 1) safe‐by‐default load if weights_only is supported
    try:
        return torch.load(path, weights_only=True)
    except TypeError:
        # older PyTorch: no weights_only argument
        pass
    except (UnpicklingError, RuntimeError):
        # come down to next stage
        pass

    # 2) plain load, may raise unpickling errors
    try:
        return torch.load(path)
    except (UnpicklingError, RuntimeError):
        # 3) whitelist Sequential then retry
        torch.serialization.add_safe_globals([torch.nn.Sequential])
        try:
            return torch.load(path)
        except (UnpicklingError, RuntimeError):
            # 4) last resort: full unpickle
            return torch.load(path, weights_only=False)

def _raw_to_tensor(x, device=None, dtype=torch.float32):
    """
    Convert numbers, tensors, file‐paths, bytes or plain strings into a torch.FloatTensor.
    Scalars → 1‐D so nn.Linear behaves itself.
    """
    device = get_device(device)

    # string input?
    if isinstance(x, str):
        if os.path.isfile(x):
            ext = x.rsplit('.', 1)[-1].lower()
            if ext == 'wav' and sf:
                data, _ = sf.read(x)
                t = torch.tensor(data, dtype=dtype, device=device)
            else:
                with open(x, 'rb') as f:
                    b = f.read()
                t = torch.tensor(list(b), dtype=dtype, device=device)
        else:
            b = x.encode('utf-8')
            t = torch.tensor(list(b), dtype=dtype, device=device)

    # raw bytes
    elif isinstance(x, (bytes, bytearray)):
        t = torch.tensor(list(x), dtype=dtype, device=device)

    # already a tensor
    elif torch.is_tensor(x):
        t = x.float().to(device)

    # numbers, lists, tuples, numpy arrays, etc.
    else:
        t = torch.tensor(x, dtype=dtype, device=device)

    # unsqueeze any scalar to 1‐D
    if t.dim() == 0:
        t = t.unsqueeze(0)

    return t

def infer(*args, output_type=None, device=None, dtype=torch.float32):
    """
    run inference on a .pt model

    usage:
      infer(in1, in2, ..., 'model.pt', [reinforcement],
            output_type='str', device='cpu', dtype=torch.float32)
    """
    inputs, model_path, reinforcement = [], None, None

    # parse args
    for arg in args:
        if isinstance(arg, str) and arg.endswith('.pt') and model_path is None:
            model_path = arg
        elif model_path and reinforcement is None and isinstance(arg, (int, float)):
            reinforcement = arg
        else:
            inputs.append(arg)

    if not model_path or not os.path.isfile(model_path):
        raise ValueError(f"model file missing or not found: {model_path!r}")

    # convert inputs
    tensors = [_raw_to_tensor(x, device=device, dtype=dtype) for x in inputs]
    if reinforcement is not None:
        tensors.append(torch.tensor(reinforcement, dtype=dtype,
                                    device=get_device(device)))

    # load & move model
    model = load_model_with_fallback(model_path)
    model = model.to(get_device(device))
    model.eval()

    with torch.no_grad():
        out = model(*tensors)

    # convert outputs
    def _convert(o):
        if torch.is_tensor(o):
            if output_type:
                if output_type not in _output_converters:
                    raise ValueError(f"unknown output_type: {output_type!r}")
                return _output_converters[output_type](o)
            return o.cpu().numpy().tolist()
        elif isinstance(o, (list, tuple)):
            return type(o)(_convert(i) for i in o)
        else:
            return o

    return _convert(out)
