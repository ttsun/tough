# TOUGH

# Changes from "Tough_mockup"
- Started from a brand new project
- "noah", "tough", "usermanage" are the new apps (self-explainatory why)
- Moved Block, BlockVars, QualifiedBlockRef to "tough"
- Moved NoahUser to "usermanage"
- All other models moved to "noah"
- "util.py" renamed to "utils.py"
- "backends.py" moved into usermanage
- settings.py and urls.py only in noah_tough, but urls should be separated into noah-sepecific and tough-sepecific (mosta re noah specific)
- Some of the imports in tough.models and usermanage.models were moved inside functions themselves and not at the top of the file. This is because django doesn't like models that cross reference eachother (django gets confused which one goes first) (There are only a couple instances of this)
- Overall rearrangement of files
