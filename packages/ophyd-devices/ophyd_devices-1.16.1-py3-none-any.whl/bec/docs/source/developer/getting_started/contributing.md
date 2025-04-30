(developer.contributing)=
# Contributing
Thank you for considering contributing to BEC! Contributions are essential for improving the project and helping it grow. 
We welcome your bug reports and feature requests via [GitLab issues](https://gitlab.psi.ch/bec/bec/-/issues?sort=created_date&state=opened), as well as contribution for documentation improvements, and code extensions or improvements.

## Reporting Bugs or Requesting Features:

- Before submitting a bug report or feature request, please check the [issue tracker](https://gitlab.psi.ch/bec/bec/issues) to avoid duplication.
- If the issue or feature hasn't been reported, open a new issue with a clear title and description. Be sure to provide steps to reproduce bugs, including _package version_ of the deployed BEC services (e.g. `bec_lib`) and information of your operating system, which will increase chances of reproducing and fixing the reported bug.

## Contributing Code:

If you are keen on contributing new code developments to BEC, please follow the guidelines on how to push code changes back into the [BEC repository](https://gitlab.psi.ch/bec).
To start with, you will first have to clone the repository to your local system as described in the [installation guide for developers](#developer.install_developer_env) and create a `bec_venv` with the developer (_[dev]_) extensions.

Afterwards, you may follow this step-by-step guide to suggest your code improvements:

1. Create a new branch for your changes:

    ```bash
    git checkout -b feature/your-feature
    ```

2. Make your changes.

3. Use Black to format your code:

    ```bash
    black --line-length=100 --skip-magic-trailing-comma .
    ```

4. Use isort to sort your imports:

    ```bash
    isort --line-length=100 --profile=black --multi-line=3 --trailing-comma .
    ```

5. Run Pylint on your code to ensure it meets coding standards:

    ```bash
    pylint your_module_or_package
    ```

6. Write tests for new features or fixed bugs, and add them to the test folder. 
We use [pytest](https://github.com/pytest-dev/pytest) within our team to test code. 

7. Follow [Conventional Commit Messages](https://www.conventionalcommits.org/en/v1.0.0/) when writing commit messages. This helps us automatically generate a changelog. For example:

    ```bash
    git commit -m "feat: add new feature"
    ```

    or

    ```bash
    git commit -m "fix: fix bug"
    ```

    or

    ```bash
    git commit -m "docs: update documentation"
    ```

8. Push your commits to the remote branch:

    ```bash
    git push origin feature/your-feature
    ```

9. Open a merge request on GitLab. Be sure to include a clear title and description of your changes. If your merge request fixes an issue, include `closes #123` in the description to automatically close the issue when the merge request is merged.

## Contributing Documentation:

- Improvements to documentation are always appreciated! If you find a typo or think something could be explained better, please open an issue or merge request.
- If you are adding new documentation, please follow the same steps as contributing code above.
