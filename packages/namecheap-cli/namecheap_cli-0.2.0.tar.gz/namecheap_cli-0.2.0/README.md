# Namecheap CLI

A command-line interface for managing Namecheap DNS records.

## Features

- List all domains in your Namecheap account
- View DNS records for a domain
- Add, update, and delete DNS records
- Interactive menu for easier management
- Secure storage of API credentials

## Installation

```bash
pip install namecheap-cli
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/connorodea/namecheap-cli.git
```

## Usage

### Interactive Mode

For the easiest usage, simply run the command without any arguments to enter interactive mode:

```bash
namecheap
```

This will display a menu similar to:

```
╭─────────────╮
│ Namecheap CLI │
╰─────────────╯

Please select an option:

[1] List domains
[2] View DNS records
[3] Add DNS record
[4] Update DNS record
[5] Delete DNS records
[0] Exit

Enter your choice [0/1/2/3/4/5] (0):
```

### Command-Line Arguments

You can also use command-line arguments for scripting or automation:

```bash
# Initialize API credentials
namecheap init

# List all domains
namecheap domains

# List DNS records for a domain
namecheap records example.com

# Add a DNS record
namecheap add -d example.com -t A -h www -v 192.168.1.1 -l 3600

# Update a DNS record
namecheap update -d example.com -t A -h www -v 192.168.1.2 -l 3600

# Delete a DNS record
namecheap delete -d example.com -t A -h www
```

### Getting Help

For more information on the available commands and options:

```bash
namecheap --help
```

## API Credentials

Upon first use, the CLI will prompt you for your Namecheap API credentials:

- API Key
- API User
- Username (usually the same as API User)
- Client IP (detected automatically)

These credentials are securely stored in `~/.namecheap/config.json` for future use.

To obtain API credentials from Namecheap:

1. Log in to your Namecheap account
2. Go to Profile > Tools > API Access
3. Enable API access and note your API key
4. Your client IP must be whitelisted in the Namecheap API settings

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Environment Variables

Instead of storing credentials in the config file, you can use environment variables:

- `NAMECHEAP_API_KEY` - Your Namecheap API key
- `NAMECHEAP_API_USER` - Your Namecheap API user
- `NAMECHEAP_USERNAME` - Your Namecheap username (optional, defaults to API_USER)
- `NAMECHEAP_CLIENT_IP` - Your client IP address (optional, auto-detected if not provided)
- `NAMECHEAP_USE_SANDBOX` - Whether to use the sandbox environment (optional, defaults to false)

You can set these variables in your shell:

```bash
export NAMECHEAP_API_KEY="your_api_key"
export NAMECHEAP_API_USER="your_api_user"
