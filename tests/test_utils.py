from src.utils.io import save_json, load_json
import os, json

def test_roundtrip(tmp_path):
    d = {"x": 1}
    p = tmp_path / "t.json"
    save_json(d, str(p))
    assert load_json(str(p)) == d
