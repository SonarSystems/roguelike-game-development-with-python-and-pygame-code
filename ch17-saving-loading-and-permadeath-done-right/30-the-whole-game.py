import json

temp = path.with_suffix(".tmp")
temp.write_text(json.dumps(data))
temp.replace(path)     # write-then-rename: a crash can't leave half a save
