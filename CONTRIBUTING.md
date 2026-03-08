# Contributing to Stem Cell Regeneration Simulator

Thank you for your interest in contributing! 🧬

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

1. Check the [issue tracker](https://github.com/Infinite-Networker/Stem-Cell-Regeneration-Simulator/issues) to see if the bug has already been reported.
2. If not, open a new issue and include:
   - A clear, descriptive title
   - Steps to reproduce the bug
   - Expected vs. actual behavior
   - Your Python version and OS

### Suggesting Enhancements

Open a new issue with the label `enhancement` and describe:
- The feature you'd like to see
- Why it would be useful
- Any implementation ideas you have

### Submitting Pull Requests

1. **Fork** the repository and create your branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Install dependencies** and make sure the code runs:
   ```bash
   pip install matplotlib
   python stem_cell_sim.py
   ```

3. **Make your changes** — keep them focused and well-commented.

4. **Test your changes** manually (and with unit tests if applicable).

5. **Commit** with a clear message:
   ```bash
   git commit -m "Add: brief description of your change"
   ```

6. **Push** to your fork and open a Pull Request against the `main` branch.

7. In the PR description, explain *what* you changed and *why*.

## Ideas for Contributions

- 🔬 Add multiple stem cell types (e.g., hematopoietic, neural)
- 🗺️ Implement spatial organization (2D grid model)
- 🌱 Add environmental factors (growth factors, nutrients, oxygen levels)
- 🎛️ Create interactive parameter sliders with `ipywidgets` or Streamlit
- 💾 Export simulation data to CSV / JSON
- ✅ Add unit tests with `pytest`
- 🌐 Create a web-based version with Streamlit
- 📊 Add more visualization types (histograms, heatmaps)

## Style Guidelines

- Follow [PEP 8](https://pep8.org/) for Python code style.
- Use descriptive variable and function names.
- Add docstrings to all public functions and classes.
- Keep functions small and focused on a single responsibility.

## Questions?

Open an issue and we'll be happy to help!
