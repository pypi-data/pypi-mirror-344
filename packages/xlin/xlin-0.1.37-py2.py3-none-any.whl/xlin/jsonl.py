import json
from typing import *

from pathlib import Path
from loguru import logger
import pandas as pd


def dataframe_to_json_list(df: pd.DataFrame):
    """
    Args:
        df (pd.DataFrame): df

    Returns:
        List[Dict[str, str]]: json list: [{"col1": "xxx", "col2": "xxx", ...}, ...]
    """
    json_list = []
    for i, line in df.iterrows():
        json_list.append(dict(line))
    return json_list


def transform_dataframe_to_json_list(df: pd.DataFrame, row_transform):
    """
    Args:
        df (pd.DataFrame): df
        row_transform : lambda row: prompt_template.format(row['query']), "", row['label']

    Returns:
        List[Dict[str, str]]: json list: [{"instruction": "xxx", "input": "xxx", "output": "xxx"}, ...]
    """
    out_list = list()
    for _, row in df.iterrows():
        instruction, input, output = row_transform(row)
        out_list.append({"instruction": instruction, "input": input, "output": output})
    return out_list


def jsonlist_to_dataframe(json_list: List[Dict[str, str]]):
    """
    Args:
        json_list (List[Dict[str, str]]): json list: [{"col1": "xxx", "col2": "xxx", ...}, ...]

    Returns:
        pd.DataFrame: df
    """
    return pd.DataFrame(json_list)


def is_jsonl(filepath: str):
    with open(filepath) as f:
        try:
            l = next(f)  # 读取一行，用来判断文件是json还是jsonl格式
            f.seek(0)
        except:
            return False

        try:
            _ = json.loads(l)
        except ValueError:
            return False  # 第一行不是json，所以是json格式
        else:
            return True  # 第一行是json，所以是jsonl格式

def load_text(filename):
    with open(filename, 'r') as f:
        return f.read()


def load_json_or_jsonl(filepath: str):
    if is_jsonl(filepath):
        return load_json_list(filepath)
    return load_json(filepath)


def load_json(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(json_list: Union[Dict[str, str], List[Dict[str, str]]], filename: str):
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        return json.dump(json_list, f, ensure_ascii=False, separators=(",", ":"), indent=2)


def load_json_list(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        json_list = []
        for i in lines:
            try:
                obj = json.loads(i.strip())
            except:
                print("格式损坏数据，无法加载")
                print(i)
                continue
            json_list.append(obj)
        return json_list


def save_json_list(json_list: List[Dict[str, str]], filename: str):
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join([json.dumps(line, ensure_ascii=False, separators=(",", ":")) for line in json_list]))


def merge_json_list(filenames: List[str], output_filename: str):
    json_list = []
    for filename in filenames:
        json_list.extend(load_json_list(filename))
    save_json_list(json_list, output_filename)


def jsonlist_dict_summary(jsonlist_dict: Dict[str, List[dict]]):
    rows = []
    for k, jsonlist in jsonlist_dict.items():
        if len(jsonlist) == 0:
            continue
        row = {
            "sheet_name": k,
            "length": len(jsonlist),
            "columns": str(list(jsonlist[0].keys())),
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    return df


def print_in_json(text: str):
    print(json.dumps({"text": text}, indent=2, ensure_ascii=False))


def apply_changes_to_jsonlist(
    jsonlist: List[Dict[str, str]],
    changes: Dict[str, Callable[[Dict[str, str]], Tuple[Literal["deleted", "updated", "unchanged"], Dict[str, str]]]],
    verbose=False,
    **kwargs,
):
    rows = jsonlist
    total_updated = 0
    total_deleted = 0
    for name, change in changes.items():
        new_rows = []
        updated = 0
        deleted = 0
        for row in rows:
            status, new_row = change(row, **kwargs)
            if status == "deleted":
                deleted += 1
                continue
            if status == "updated":
                updated += 1
            new_rows.append(new_row)
        rows = new_rows
        msgs = []
        if updated > 0:
            total_updated += updated
            msgs += [f"updated {updated}"]
        if deleted > 0:
            total_deleted += deleted
            msgs += [f"deleted {deleted}"]
        if verbose and updated > 0 or deleted > 0:
            logger.info(f"{name}: {', '.join(msgs)}, remained {len(new_rows)} rows.")
    return rows, total_updated, total_deleted


def apply_changes_to_paths(
    paths: List[Path],
    changes: Dict[str, Callable[[Dict[str, str]], Tuple[Literal["deleted", "updated", "unchanged"], Dict[str, str]]]],
    verbose=False,
    save=False,
    load_json=load_json,
    save_json=save_json,
    **kwargs,
):
    total_updated = 0
    total_deleted = 0
    for path in paths:
        if verbose:
            print("checking", path)
        jsonlist = load_json(path)
        kwargs["path"] = path
        new_jsonlist, updated, deleted = apply_changes_to_jsonlist(jsonlist, changes, verbose, **kwargs)
        msgs = [f"total {len(jsonlist)} -> {len(new_jsonlist)}"]
        if updated > 0:
            total_updated += updated
            msgs += [f"updated {updated}"]
        if deleted > 0:
            msgs += [f"deleted {deleted}"]
            total_deleted += deleted
        if updated > 0 or deleted > 0:
            print(f"{path}: {', '.join(msgs)}")
            if save:
                if len(new_jsonlist) > 0:
                    save_json(new_jsonlist, path)
                else:
                    path.unlink()
    print(f"total: updated {total_updated}, deleted {total_deleted}")


def backup_current_output(row: Dict[str, str], output_key="output"):
    if "old_output" in row:
        for i in range(1, 10):
            if f"old_output{i}" not in row:
                row[f"old_output{i}"] = row[output_key]
                break
    else:
        row["old_output"] = row[output_key]
    return row


def backup_and_set_output(row: Dict[str, str], output: str):
    backup_current_output(row)
    row["output"] = output
    return row


def generator_from_paths(paths: List[Path], load_data: Callable[[Path], List[Dict[str, Any]]] = load_json):
    for path in paths:
        jsonlist: List[Dict[str, Any]] = load_data(path)
        for row in jsonlist:
            yield path, row



def append_to_json_list(data: list[dict], file_path: Union[str, Path]):
    """Append a list of dictionaries to a JSON file."""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if file_path.exists() and file_path.is_dir():
        print(f"{file_path} is a directory, not a file.")
        return
    with open(file_path, "a", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n")


def row_to_json(row: dict) -> dict:
    """Convert a row to a JSON object."""
    new_row = {}
    for k, v in row.items():
        if isinstance(v, dict):
            new_row[k] = row_to_json(v)
        elif isinstance(v, list):
            new_row[k] = [row_to_json(item) for item in v]
        elif isinstance(v, pd.DataFrame):
            new_row[k] = [row_to_json(item) for item in v.to_dict(orient="records")]
        else:
            new_row[k] = v

    return new_row


def generator_from_json(path):
    jsonlist = load_json(path)
    for line in jsonlist:
        yield line


def generator_from_jsonl(path):
    jsonlist = load_json_list(path)
    for line in jsonlist:
        yield line
