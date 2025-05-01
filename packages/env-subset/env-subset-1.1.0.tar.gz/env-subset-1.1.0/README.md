# env-subset -- Run a command with a subset of the environment
**@readwithai** - [X](https://x.com/readwithai) - [blog](https://readwithai.substack.com/) - [machine-aided reading](https://www.reddit.com/r/machineAidedReading/) - [📖](https://readwithai.substack.com/p/what-is-reading-broadly-defined)[⚡️](https://readwithai.substack.com/s/technical-miscellany)[🖋️](https://readwithai.substack.com/p/note-taking-with-obsidian-much-of)

env-subset is a swiss army knife for manipulating the environment used to run a command, written because `env` did not have the options I wanted and the other ways of doing things was unwieldy


## Motivation
Programs change their behaviour based on the environment. It is therefore natural to want to be able to control the environment to control the program for debug and standard use. There are some tools for this - namely `env` and `printenv` but they are a little cumbersome.

This program is effectively "`env` with a lot of flags" to give you more control over the environment. This program is also more consistent than env and provides documentation via `--help` making it easier to install.

It is also released as open source code and can be installed with one (or two) lines on most systems.

## Alternatives and prior work
You can hack up something quite similar to this use `env`, `printenv`, `grep`, `bash -c` etc. But this requires quite a lot of typing and is error prone.

If you want to change a single environment variable you can use e.g. `env VAR=value printenv`, bash and zsh can do this with `VAR=value printenv`. If you want to run without an environemt `env -i printenv`. If you want to run with a fixed environment you can use `env -i env VAR=Value printenv`. If you want to read environment variables from a file you can use `env -i bash -c "source $file; printenv"`

This is vaguely related to the idea of [dotenv](https://www.npmjs.com/package/dotenv) and [python-dotenv](https://pypi.org/project/python-dotenv/).

For complete control, you can write your own program in python using the `env` option of `subprocess` - like this tool does.

## Installation
You can install env-subset using [pipx](https://github.com/pypa/pipx):
```
pipx install env-subset
```
# Usage
Run `ls` is just the `LANGUAGE` environment. You can also use `--variable`
```
env-subset -e LANGUAGE ls
```

Run `ls` with both `LANG` and `LANGUAGE`
```
env-subset -e LANGUAGE ls
```

Run `xterm` with all the environment variables starting with X. This uses a regular expression. You can also use `-r` or `--regexp`
```
env-subset -e '/^X/' xterm
```

Run `ls` without the LANGUAGE enviornment variable - but with everything else. You can also use `--exclude`
```
env-subset -x -e LANGUAGE ls
```

Run a command with flags.
```
env-subset -e LANGUAGE -- python -m pdb
```

Set language to German:
```
env-subset -e LANGUAGE=de -e LANG=de -- python -m pdb
```

Read settings from a file. This can be generated with `printenv` but has some additional features. You can write the variable name along to take the variable from the outer scope. Write regular expressions of the form `^` to write a regular expression or `//` for a regular expression.

```
env-subset -f environment.env printenv
```

## Debugging
`env-subset printenv`, `env-subset printenv | grep`, `env-subset printenv | fzf` are useful commands for working out what `env-subset` is doing.


## About me
I am **@readwithai**. I create tools for reading, research and agency sometimes using the markdown editor [Obsidian](https://readwithai.substack.com/p/what-exactly-is-obsidian).

I also create a [stream of tools](https://readwithai.substack.com/p/my-productivity-tools) that are related to carrying out my work.

I write about lots of things - including tools like this - on [X](https://x.com/readwithai).
My [blog](https://readwithai.substack.com/) is more about reading and research and agency.
