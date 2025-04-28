## cdf 

### Fixed

- You can now set the default encoding Toolkit should use when reading
files. This is useful on Windows machines, where special characters like
`ã` and `é` can be scrambled when running `cdf build` + `cdf deploy` if
a file is `utf-8` encoded while the default encoding is `cp1252`. You
can set the default encoding with `cdf.file_encoding = ""` in the
`cdf.toml` file

## templates

No changes.