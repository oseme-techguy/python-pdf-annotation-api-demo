"""PDF Annotation API application - entrypoint."""

from app import Application, run_api

if __name__ == '__main__':
    APP = Application()
    run_api(APP)
