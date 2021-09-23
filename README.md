# ssh-helper

ssh-helper is a cli tool to manage ssh access to your fleet of machines.

## Installation

```bash
# Clone repo
git clone https://github.com/xgaia/ssh-helper.git
cd ssh-helper
# Install
pip install -e .
````

## Usage

### Configure

First, create a `servers.yaml` file in `~/config/sshh/servers.yaml`. You can use `example.yaml` as a template. 

```bash
cp example.yaml ~/config/sshh.servers.yaml
vim ~/config/sshh.servers.yaml
```

### Use

Get the help

```bash
sshh --help
```

List available machines

```bash
sshh list
```

```
Name           Group                    ssh                                Port
-------------------------------------------------------------------------------
pi             personal                 jdoe@raspberry.example.org         2222
skynet         work/prod                john@192.168.0.1                   22
backup         work/backup              john@192.168.0.2                   2223
```

List machines on a specific group


```bash
sshh list -g work
```

```
Name           Group                    ssh                                Port
-------------------------------------------------------------------------------
skynet         work/prod                john@192.168.0.1                   22
backup         work/backup              john@192.168.0.2                   2223
```

List machines on a specific group and subgroup


```bash
sshh list -g work/prod
```

```
Name           Group                    ssh                                Port
-------------------------------------------------------------------------------
skynet         work/prod                john@192.168.0.1                   22
```

Connect to a machine

```bash
sshh ssh skynet
```

Connect to a machine using `root` user


```bash
# connect to a machine with root user
sshh ssh skynet --root
```