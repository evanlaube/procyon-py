
# Contributing

Thank you for consider making a contribution to Procyon! Any contribution, no matter the size, 
is a huge help in making a better library for all to use. All contributions are welcome from new features
to improved documentation, or even just fixing my many typos.

To contribute to Procyon, in order to improve efficiency for everyone, please follow
these guidelines:

## How to contribute
1. Fork the repository and create your own branch from `main`
2. Clone the forked repository to your local machine.
```bash
git clone https://github.com/[YOUR USERNAME]/procyon-py
```
3. Make your changes and ensure that the code style and formatting guidelines are followed.
4. Ensure that the code runs properly before committing.
5. Update the documentation to reflect any changes or new features.
6. Commit your changes with a descriptive commit message.
7. Push your changes to your forked repository
```bash
git push origin [YOUR_BRANCH_NAME]
```
8. Submit a pull request to the `main` branch of the original repository

## Running the library in development mode
Usually, the library is installed using the command:
```bash
pip install procyon-py
```
However, when planning on making changes to the library locally and test them, the 
library must be installed in an editable mode so that the modified version of the library
is used when importing procyon. 

To do this, first uninstall the current installation of
Procyon:
```bash
pip uninstall procyon-py
```

Then, if you have not already cloned the repository, clone it
```bash
git clone https://github.com/[YOUR_USERNAME/procyon-py
```

Next, navigate to the root of the project:
```bash
cd procyon-py
```

Finally, run the following command to install the library in editable mode
```bash
pip install -e .
```
Now, any changes made will reflect when importing Procyon.

#### Switching back to regular installation
Note that this version installed in editable mode is not as performant as the regular install. If 
you even plan to stop development and simply use Procyon, uninstall this version and reinstall the
regular way.

```bash
pip uninstall procyon-py
pip install procyon-py
```


## Code style and formatting
- Please follow the existing code style and formatting conventions.
- Use meaningful variable and function names - longer names are usually preferrered to shorter ones, within reason.
- Write clear and concise comments to explain complex code segments. While comments are preffered, they are not always necessary

#### Sidenote
Through this project, I have been using camelCase for member variables, which I know is not normal convention
in Python. I understand that most python developers prefer to use snake_case. I am not against new contributions using
snake_case in the prject, as I do plan on eventually converting all member variables and methods to using snake_case

## Reporting Issues
If you encounter any unusual bugs, issues, or have suggestions for improvements, plesae feel free to [open an issue](https://github.com/evanlaube/procyon-py/issues) on GitHub.

## THANK YOU
I could not be more appreciative for you taking your own time to consider contributing to Procyon!
I do truly think that this library has value in creating simple applications quickly, and can be 
very useful for making simple interactive utilities
