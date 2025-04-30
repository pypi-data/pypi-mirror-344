
# Lithio - Python clone of GNU install

Lithio is a Python clone of the GNU `install` command, designed to provide a safe, flexible, and cross-platform solution for installing files and managing file permissions in various environments.

### Installation

#### To install, run (be aware of what the `install.sh` script does):
```bash
bash install.sh
```

> **Note:** The `install.sh` script sets up the package and installs necessary dependencies. Review the script before running it to understand what actions it performs.

#### To install files:
Once installed, you can use `lithio` to install files:

```bash
lithio file1 file2 /path/to/destination
```

This will copy `file1` and `file2` to the specified destination directory.

> **Note:** If you used `install.sh` to install the package, you can install files that require elevated privileges `sudo -E lithio`

#### To install files with `sudo`:

```bash
sudo -E lithio file1 file2 /path/to/destination
```

The `-E` flag preserves the user's environment, which is useful when running the command with `sudo`.

### Features
- **Simple command-line usage**: Install files with ease and flexibility.
- **Checksum validation**: You can validate file integrity using the `--checksum <checksum_file>` option with `--checksum-type`. The `<checksum_file>` should contain a list of file names and their associated hashes in the format `<file_name>:<file_hash>\n`.
- **Usability in scripts**: `lithio` does not require any kind of user interaction, making it ideal for automation.
- **Extendable**: Easily adaptable for future functionalities.
- **More**: More information can be found in the `man` page `man lithio`

### Contributing

Contributions are welcome! If you have suggestions, bug reports, or improvements, please open an issue or submit a pull request.

1. Fork the repository
2. Create a new branch (\`git checkout -b feature-branch\`)
3. Commit your changes (\`git commit -am 'Add new feature'\`)
4. Push to the branch (\`git push origin feature-branch\`)
5. Create a new pull request

Make sure to add tests and documentation for your changes.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Contact

For questions, you can reach me at [voyager-2019@outlook.com](mailto:voyager-2019@outlook.com).

### Acknowledgments

- Inspired by the GNU \`install\` command
- Thanks to the contributors who helped improve this project!