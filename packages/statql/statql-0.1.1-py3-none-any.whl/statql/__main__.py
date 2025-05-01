import os
import sys
import streamlit.web.cli as stcli


def main():
    sys.argv = ["streamlit", "run", os.path.join(os.path.dirname(__file__), "app", "app.py")]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
