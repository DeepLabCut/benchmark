from deeplabcut.benchmark.cli import main
import deeplabcut.benchmark.utils as __utils

results = __utils.import_submodules("benchmark", recursive=True)

if __name__ == "__main__":
    main()

