# sshh: ssh-helper

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

Get the help

```bash
sshh --help
```

Add some machines

```bash
sshh add pi -a jdoe@raspberry.example.org -p 2222 -g personal
sshh add skynet -a john@192.168.0.1 -g work/prod
sshh add backup -a john@192.168.0.2  -p 2223 -g work/backup
```

List available machines

```bash
sshh list
```

```
Name           Group                    ssh                                Port
-------------------------------------------------------------------------------
pi             personal                 jdoe@raspberry.example.org         2222
backup         work/backup              john@192.168.0.2                   2223
skynet         work/prod                john@192.168.0.1                   22
```

List machines on a specific group


```bash
sshh list -g work
```

```
Name           Group                    ssh                                Port
-------------------------------------------------------------------------------
backup         work/backup              john@192.168.0.2                   2223
skynet         work/prod                john@192.168.0.1                   22
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
