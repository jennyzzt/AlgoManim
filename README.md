### Installation
Assumes setup on Ubuntu Linux.

First, install Python and Python Dev Tools (if not already installed)
```bash
sudo apt install python3 python3-dev
```

Next, install all system library dependencies of Manim (this will consume quite a bit of disk space)

```bash
sudo apt install sox ffmpeg libcairo2 libcairo2-dev texlive-full
```
> For alternative system setup, please check the [official Manim documentation](https://manim.readthedocs.io/en/latest/installation/index.html#) out

Lastly, set up a virtual environment and install the Python dependencies. The command line should now be prefaced by `(venv)`.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Verify installation by running the following command, which will produce preview files under `./media`.
```bash
python3 -m manim example_scenes.py SquareToCircle -pl
```

### Installation
You can run the video-rendering GUI as follows:
```bash
python3 -m cmdgui
```

### Docs
You can find documentation on how to use the library in `docs/`.

### Coding style and conventions
All Python code should adhere to [PEP8](https://www.python.org/dev/peps/pep-0008/). Pylint is used to enforce this, so it would probably be a good idea to select the linter in your editor if it allows you to.
If there are any linting rules that you want to exclude (for good reason), disable it in `.pylintrc`.
In order to pre-empt pipeline failure, please run `pytest -v --cov=algomanim` and `pylint *` locally before pushing.

Provisionally, the project folder structure is as follows:
`./algomanim` is the main folder where project source files should go.
`./tests` will contain the test files (with filenames prefaced by `test_`).
All generated files should be added to `./.gitignore`, please check before committing!

Feel free to update this README as we go along.