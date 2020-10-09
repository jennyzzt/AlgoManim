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

Verify installation by running the following command, which will produce preview files in the folder `media`
```bash
python3 -m manim example_scenes.py SquareToCircle -pl
```