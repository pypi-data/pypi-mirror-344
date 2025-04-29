import os
import torch
from pickle import UnpicklingError
# optional WAV support
try:
    import soundfile as sf
except ImportError:
    sf = None
detected_device = "cuda" if torch.cuda.is_available() else "cpu"
# registry for output converters
_output_converters = {
    'int': lambda t: int(t.item()),
    'float': lambda t: float(t.item()),
    'str': lambda t: t.cpu().numpy().tolist() if t.numel() > 1 else str(t.item()),
    'binary': lambda t: t.cpu().numpy().tobytes(),
}


def register_output_converter(name, fn):
    """
    register a custom output converter under `name`
    fn: torch.Tensor -> any
    """
    _output_converters[name] = fn

def load_model_with_fallback(path):
    try:
        # 1) safe-by-default load (weights_only=True in PyTorch 2.6+)
        return torch.load(path)
    except UnpicklingError:
        # 2) try whitelisting the missing class under safe_globals
        try:
            torch.serialization.add_safe_globals([torch.nn.modules.container.Sequential])
            return torch.load(path)
        except UnpicklingError:
            # 3) last resort: full unpickling (NOT safe unless you trust the file)
            return torch.load(path, weights_only=False)

def _raw_to_tensor(x):
    """
    Convert numbers, tensors, file-paths, bytes or plain strings into a torch.FloatTensor.
    - file paths → file bytes (or wav samples)
    - bytes/bytearray → raw bytes
    - other strings → UTF-8 bytes of the text
    - numbers/lists/etc → torch.tensor
    Scalars (0-D) are unsqueezed to 1-D so nn.Linear doesn’t complain.
    """
    # 1) string input?
    if isinstance(x, str):
        if os.path.isfile(x):
            # a) actual file on disk
            ext = x.rsplit('.', 1)[-1].lower()
            if ext == 'wav' and sf:
                data, _ = sf.read(x)
                t = torch.tensor(data, dtype=torch.float32,device=detected_device)
            else:
                with open(x, 'rb') as f:
                    b = f.read()
                t = torch.tensor(list(b), dtype=torch.float32, device=detected_device)
        else:
            # b) plain text → UTF-8 bytes
            b = x.encode('utf-8')
            t = torch.tensor(list(b), dtype=torch.float32,device=detected_device)

    # 2) raw bytes
    elif isinstance(x, (bytes, bytearray)):
        t = torch.tensor(list(x), dtype=torch.float32,device=detected_device)

    # 3) already a tensor
    elif torch.is_tensor(x):
        t = x.float()

    # 4) numbers, lists, tuples, numpy arrays, etc.
    else:
        t = torch.tensor(x, dtype=torch.float32,device=detected_device)

    # 5) unsqueeze any scalar into a 1-D tensor
    if t.dim() == 0:
        t = t.unsqueeze(0)

    return t


def nn(*args, output_type=None):
    """
    run inference on a .pt model

    usage:
      frp.nn(in1, in2, ..., 'model.pt', [reinforcement], output_type='str')
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

    tensors = [_raw_to_tensor(x) for x in inputs]
    if reinforcement is not None:
        tensors.append(torch.tensor(reinforcement))

    model = load_model_with_fallback(model_path)
    model.eval()
    with torch.no_grad():
        out = model(*tensors)

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
