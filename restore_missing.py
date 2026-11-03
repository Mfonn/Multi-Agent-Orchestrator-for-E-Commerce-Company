import ast

NEWSTARTER = "agent_orchestrator_NEWSTARTER.py"
CURRENT = "src/agent_orchestrator.py"
BUILDERS = {"build_inventory_agent", "build_refund_agent", "build_policy_agent",
            "build_communication_agent", "build_orchestrator_agent"}

new_src = open(NEWSTARTER, encoding="utf-8").read()
cur_src = open(CURRENT, encoding="utf-8").read()


def region(text):
    # The same area my splice script replaced
    start = text.index("def build_inventory_agent")
    guard = text.index("def create_guardrail")
    close = text.rfind("# ═", 0, guard)
    opening = text.rfind("# ═", 0, close)
    return start, opening


def name_of(node):
    return getattr(node, "name", None)


n_start, n_end = region(new_src)
start_line = new_src.count("\n", 0, n_start) + 1
end_line = new_src.count("\n", 0, n_end) + 1
lines = new_src.splitlines(keepends=True)

current_names = {name_of(n) for n in ast.parse(cur_src).body if name_of(n)}

chunks, restored = [], []
for node in ast.parse(new_src).body:
    first = min([d.lineno for d in getattr(node, "decorator_list", [])] + [node.lineno])
    if not (start_line <= first < end_line):
        continue
    name = name_of(node)
    if name in BUILDERS or name in current_names:
        continue
    chunks.append("".join(lines[first - 1:node.end_lineno]))
    restored.append(name or "(a top-level statement)")

if not chunks:
    print("Nothing was missing.")
else:
    _, cur_end = region(cur_src)
    result = cur_src[:cur_end] + "\n\n".join(chunks) + "\n\n" + cur_src[cur_end:]
    open(CURRENT, "w", encoding="utf-8").write(result)
    print("Restored:", ", ".join(restored))
    print("TODO markers in the restored code:", sum(c.count("# TODO") for c in chunks))