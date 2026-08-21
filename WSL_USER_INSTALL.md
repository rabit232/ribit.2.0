# Ribit 2.0: No-Sudo User-Level WSL Installation

This guide installs Ribit’s declared Python dependencies into a **user-owned target directory**. It does not use `sudo`, the system package manager, or a global Python installation.

## Why use a target directory?

On the tested WSL runtime, `python3 -m venv` is unavailable because the optional Ubuntu `python3-venv` package is not installed. Installing it would require a system-level change, so this guide deliberately uses pip’s `--target` option instead.

## Install

From the repository root, run:

```bash
TARGET="$HOME/.local/share/ribit-ghostos-user-install/ribit_compatible_site"
mkdir -p "$TARGET"
python3 -m pip install --upgrade --target "$TARGET" -r requirements-wsl-user.txt
```

Use the installed dependencies with the local source tree by setting `PYTHONPATH` only for the command you run:

```bash
PYTHONPATH="$TARGET:$PWD" python3 -c "from ribit_2_0.mock_llm_wrapper import MockRibit20LLM; print(MockRibit20LLM().get_decision('Introduce yourself'))"
```

The command above returns a mock action envelope. It does **not** grant permission to run commands, control a GUI, send messages, or access hardware. Any action text should be treated as untrusted data unless an application has separately applied an explicit authorization policy.

## Tested compatibility overlay

`requirements-wsl-user.txt` includes the ordinary `requirements.txt` and adds:

```text
deltachat>=1.40.1,<2
pytest>=8.0,<9.0
```

This is necessary because DeltaBot 0.8 imports a DeltaChat 1.x API removed by DeltaChat 2.x. In the verified no-sudo installation, this resolved to `deltabot==0.8.0`, `deltachat==1.155.6`, and `pytest==8.4.2`.

## Scope

The optional ROS dependencies remain commented out in the main requirements file and are not included here. This guide does not configure Matrix credentials, Matrix E2EE, DeltaChat accounts, web access, GUI control, process execution, or robot hardware.
