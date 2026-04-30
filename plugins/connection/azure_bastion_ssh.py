# Copyright (c) 2025 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
    name: azure_bastion_ssh
    short_description: Connect to a private Azure VM through Azure Bastion via a local tunnel.
    version_added: "3.17.0"
    description:
        - This connection plugin enables Ansible to reach VMs in private Azure virtual networks by tunneling SSH through an Azure Bastion host.
        - On first use per host the plugin spawns C(az network bastion tunnel) as a background subprocess on the controller, waits for the local
          port to be ready, and then delegates to the standard C(ssh) connection plugin which it subclasses. All standard SSH features
          (SFTP, ControlMaster, become, etc.) work as usual.
        - The Azure CLI (C(az)) and the C(bastion) extension must be installed on the Ansible controller. The Bastion resource must use
          the Standard SKU (or higher) with C(enableTunneling=true).
        - Only SSH key authentication is supported in this version.
        - All standard C(ssh) connection plugin variables are honored (for example C(ansible_user), C(ansible_ssh_private_key_file),
          C(ansible_ssh_common_args)). Their option definitions are inherited from the built-in C(ssh) connection plugin at runtime.
    author:
        - Ansible Cloud Content Team (@ansible-collections)
    requirements:
        - The Azure CLI (V(az)) installed on the Ansible controller.
        - The V(bastion) Azure CLI extension (V(az extension add --name bastion)).
        - Bastion SKU Standard or higher with native client tunneling enabled.
    options:
        azure_bastion_name:
            description: Name of the Azure Bastion host to tunnel through.
            type: str
            required: true
            vars:
                - name: ansible_azure_bastion_name
        azure_bastion_resource_group:
            description: Resource group containing the Azure Bastion host.
            type: str
            required: true
            vars:
                - name: ansible_azure_bastion_resource_group
        azure_bastion_subscription:
            description:
                - Azure subscription ID or name in which the Bastion host
                  lives. If unset, the C(az) CLI's currently selected
                  subscription is used.
            type: str
            vars:
                - name: ansible_azure_bastion_subscription
        azure_bastion_target_resource_id:
            description:
                - Full ARM resource ID of the target VM to connect to,
                  e.g.
                  V(/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Compute/virtualMachines/<vm>).
            type: str
            required: true
            vars:
                - name: ansible_azure_bastion_target_resource_id
        azure_bastion_target_port:
            description: Port on the target VM to forward (SSH).
            type: int
            default: 22
            vars:
                - name: ansible_azure_bastion_target_port
        azure_bastion_local_port:
            description:
                - Local TCP port to bind the tunnel to. If unset, a free
                  ephemeral port is chosen automatically.
                - When running plays in parallel against many hosts you
                  must leave this unset (or unique per host) to avoid
                  cross-host port collisions.
            type: int
            vars:
                - name: ansible_azure_bastion_local_port
        azure_bastion_tunnel_timeout:
            description: Seconds to wait for the local tunnel port to be ready.
            type: int
            default: 30
            vars:
                - name: ansible_azure_bastion_tunnel_timeout
        azure_bastion_az_path:
            description: Path to the C(az) CLI binary on the controller.
            type: str
            default: az
            vars:
                - name: ansible_azure_bastion_az_path
        # ---------------------------------------------------------------
        # Proxy options for the underlying ``ssh`` connection plugin.
        #
        # Ansible's task executor only forwards variables to a connection plugin's ``set_options(var_options=...)`` if those variables are
        # declared in the plugin's own option spec (see ``ansible.executor.task_executor._set_plugin_options``). So we
        # have to re-declare the standard ssh-plugin vars here to make ``ansible_user``, ``ansible_ssh_private_key_file``, etc. flow
        # through. 
        # 
        # The values land in ``self._options`` under the canonical keys (``remote_user``, ``private_key_file``, ...) where the parent ssh 
        # plugin's ``get_option`` reads them.
        # ---------------------------------------------------------------
        remote_user:
            description: Username to log in as on the target host (forwarded to the ssh plugin).
            type: str
            vars:
                - name: ansible_user
                - name: ansible_ssh_user
            env:
                - name: ANSIBLE_REMOTE_USER
            ini:
                - section: defaults
                  key: remote_user
        password:
            description: Authentication password for the C(remote_user). SSH key auth is preferred for v1.
            type: str
            vars:
                - name: ansible_password
                - name: ansible_ssh_pass
                - name: ansible_ssh_password
        private_key_file:
            description: Private key file used by ssh.
            type: path
            vars:
                - name: ansible_private_key_file
                - name: ansible_ssh_private_key_file
            env:
                - name: ANSIBLE_PRIVATE_KEY_FILE
            ini:
                - section: defaults
                  key: private_key_file
        ssh_args:
            description: Arguments to pass to all ssh CLI tools.
            type: str
            default: '-C -o ControlMaster=auto -o ControlPersist=60s'
            vars:
                - name: ansible_ssh_args
            env:
                - name: ANSIBLE_SSH_ARGS
            ini:
                - section: 'ssh_connection'
                  key: 'ssh_args'
        ssh_common_args:
            description: Common extra args for all ssh CLI tools.
            type: str
            default: ''
            vars:
                - name: ansible_ssh_common_args
            env:
                - name: ANSIBLE_SSH_COMMON_ARGS
            ini:
                - section: 'ssh_connection'
                  key: 'ssh_common_args'
        ssh_extra_args:
            description: Extra exclusive to the ssh CLI.
            type: str
            default: ''
            vars:
                - name: ansible_ssh_extra_args
            env:
                - name: ANSIBLE_SSH_EXTRA_ARGS
            ini:
                - section: 'ssh_connection'
                  key: 'ssh_extra_args'
        sftp_extra_args:
            description: Extra exclusive to the sftp CLI.
            type: str
            default: ''
            vars:
                - name: ansible_sftp_extra_args
            env:
                - name: ANSIBLE_SFTP_EXTRA_ARGS
            ini:
                - section: 'ssh_connection'
                  key: 'sftp_extra_args'
        scp_extra_args:
            description: Extra exclusive to the scp CLI.
            type: str
            default: ''
            vars:
                - name: ansible_scp_extra_args
            env:
                - name: ANSIBLE_SCP_EXTRA_ARGS
            ini:
                - section: 'ssh_connection'
                  key: 'scp_extra_args'
        ssh_executable:
            description: Location of the ssh binary.
            type: string
            default: ssh
            vars:
                - name: ansible_ssh_executable
            env: [{name: ANSIBLE_SSH_EXECUTABLE}]
            ini:
                - section: ssh_connection
                  key: ssh_executable
        host_key_checking:
            description: Determines if ssh should check host keys.
            type: boolean
            vars:
                - name: ansible_host_key_checking
                - name: ansible_ssh_host_key_checking
            env:
                - name: ANSIBLE_HOST_KEY_CHECKING
                - name: ANSIBLE_SSH_HOST_KEY_CHECKING
            ini:
                - section: defaults
                  key: host_key_checking
                - section: ssh_connection
                  key: host_key_checking
        timeout:
            description: SSH connection timeout in seconds.
            type: integer
            default: 10
            vars:
                - name: ansible_ssh_timeout
                - name: ansible_timeout
            env:
                - name: ANSIBLE_TIMEOUT
                - name: ANSIBLE_SSH_TIMEOUT
            ini:
                - key: timeout
                  section: defaults
                - key: timeout
                  section: ssh_connection
        pipelining:
            description: Enable pipelining for the ssh plugin.
            type: bool
            vars:
                - name: ansible_pipelining
                - name: ansible_ssh_pipelining
            env:
                - name: ANSIBLE_PIPELINING
                - name: ANSIBLE_SSH_PIPELINING
            ini:
                - section: connection
                  key: pipelining
                - section: ssh_connection
                  key: pipelining
'''

EXAMPLES = '''
# Inventory:
#
# [private_vms]
# webapp-01 ansible_host=10.0.1.4 \
#     ansible_azure_bastion_target_resource_id=/subscriptions/.../virtualMachines/webapp-01
#
# [private_vms:vars]
# ansible_connection=azure.azcollection.azure_bastion_ssh
# ansible_user=azureuser
# ansible_ssh_private_key_file=~/.ssh/id_rsa
# ansible_azure_bastion_name=my-bastion
# ansible_azure_bastion_resource_group=my-network-rg
'''

import atexit
import threading

from ansible import constants as C
from ansible.errors import AnsibleConnectionFailure, AnsibleError
from ansible.plugins.connection.ssh import Connection as SSHConnection
from ansible.utils.display import Display

from ansible_collections.azure.azcollection.plugins.plugin_utils.bastion_tunnel import (
    BastionTunnelError,
    check_az_available,
    check_bastion_extension,
    drain_stream_to_buffer,
    is_port_in_use,
    pick_free_port,
    start_tunnel,
    terminate_tunnel,
    wait_for_port,
)

display = Display()

# Strong references to live tunnel subprocesses so an atexit hook can
# terminate them if a connection close path is skipped (e.g. controller
# SIGINT). Strong (not weak) so Popen objects aren't GC'd prematurely.
_LIVE_TUNNELS = set()
_LIVE_TUNNELS_LOCK = threading.Lock()


def _atexit_cleanup():
    with _LIVE_TUNNELS_LOCK:
        procs = list(_LIVE_TUNNELS)
        _LIVE_TUNNELS.clear()
    for proc in procs:
        try:
            terminate_tunnel(proc, grace_seconds=2)
        except Exception:
            pass


atexit.register(_atexit_cleanup)


class Connection(SSHConnection):
    """SSH-via-Azure-Bastion connection plugin.

    Subclasses the built-in C(ssh) plugin. On the first call to
    :meth:`_connect` it brings up a local tunnel via
    ``az network bastion tunnel`` and rewrites the connection target to
    ``127.0.0.1:<local_port>`` before delegating up the MRO. Subsequent
    calls reuse the same tunnel. :meth:`close` tears it down.
    """

    transport = "azure.azcollection.azure_bastion_ssh"
    has_pipelining = True

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        self._bastion_tunnel_proc = None
        self._bastion_local_port = None
        self._bastion_started = False
        self._bastion_stderr_buf = bytearray()

    # -- option machinery -------------------------------------------------
    #
    # Our DOCUMENTATION re-declares the most-used ``ssh`` connection plugin
    # options (remote_user, private_key_file, ssh_*, host_key_checking,
    # timeout, pipelining, control_path[_dir], reconnection_retries, etc.)
    # so Ansible's task executor passes ``ansible_user`` /
    # ``ansible_ssh_private_key_file`` / etc. through to our
    # ``set_options``. Their values then land in ``self._options`` under
    # the canonical keys (``remote_user``, ``private_key_file``, ...) where
    # the parent ssh plugin's ``get_option`` reads them.
    #
    # For any option ssh declares that we did NOT re-declare,
    # ``get_option`` falls back to resolving against the ssh plugin's
    # config so parent-class methods don't blow up.

    def get_option(self, option, hostvars=None):
        if option in self._options:
            return self._options[option]
        try:
            return super(Connection, self).get_option(option, hostvars=hostvars)
        except KeyError:
            try:
                value, _origin = C.config.get_config_value_and_origin(
                    option, plugin_type='connection', plugin_name='ssh', variables=hostvars,
                )
            except AnsibleError as exc:
                raise KeyError(str(exc))
            self._options[option] = value
            return value

    # -- tunnel lifecycle -------------------------------------------------

    def _ensure_tunnel(self):
        if (self._bastion_started
                and self._bastion_tunnel_proc is not None
                and self._bastion_tunnel_proc.poll() is None
                and is_port_in_use(self._bastion_local_port)):
            return

        # If a previous tunnel died or the local port stopped listening,
        # tear it down before bringing up a new one.
        if self._bastion_tunnel_proc is not None:
            self._teardown_tunnel()

        bastion_name = self.get_option("azure_bastion_name")
        resource_group = self.get_option("azure_bastion_resource_group")
        subscription = self.get_option("azure_bastion_subscription")
        target_id = self.get_option("azure_bastion_target_resource_id")
        target_port = self.get_option("azure_bastion_target_port")
        local_port = self.get_option("azure_bastion_local_port")
        timeout = self.get_option("azure_bastion_tunnel_timeout")
        az_path = self.get_option("azure_bastion_az_path")

        try:
            az_resolved = check_az_available(az_path)
            check_bastion_extension(az_resolved)
        except BastionTunnelError as exc:
            raise AnsibleConnectionFailure(str(exc))

        if local_port:
            if is_port_in_use(local_port):
                raise AnsibleConnectionFailure(
                    "azure_bastion_local_port=%d is already in use on 127.0.0.1. "
                    "Pick a different port or leave it unset to auto-allocate. "
                    "Note: when running against multiple hosts in parallel, a fixed "
                    "port set as a group var would cause cross-host collisions; "
                    "leave azure_bastion_local_port unset for parallel runs."
                    % local_port
                )
        else:
            local_port = pick_free_port()

        display.vvv(
            "azure_bastion_ssh: starting tunnel via bastion '%s' (rg=%s) -> %s:%d on 127.0.0.1:%d"
            % (bastion_name, resource_group, target_id, target_port, local_port),
            host=self.get_option("host"),
        )

        proc = None
        try:
            proc = start_tunnel(
                az_path=az_resolved,
                bastion_name=bastion_name,
                resource_group=resource_group,
                target_resource_id=target_id,
                target_port=target_port,
                local_port=local_port,
                subscription=subscription,
            )
            with _LIVE_TUNNELS_LOCK:
                _LIVE_TUNNELS.add(proc)
            wait_for_port(local_port, timeout=timeout, proc=proc)
        except BastionTunnelError as exc:
            if proc is not None:
                terminate_tunnel(proc)
                with _LIVE_TUNNELS_LOCK:
                    _LIVE_TUNNELS.discard(proc)
            raise AnsibleConnectionFailure("Azure Bastion tunnel setup failed: %s" % exc)

        # Drain stdout/stderr so they don't fill the pipe buffer and stall
        # the long-running tunnel process. Capture stderr into a bounded
        # buffer for diagnostics if the tunnel dies later.
        self._bastion_stderr_buf = bytearray()
        if proc.stdout is not None:
            drain_stream_to_buffer(proc.stdout, bytearray())
        if proc.stderr is not None:
            drain_stream_to_buffer(proc.stderr, self._bastion_stderr_buf)

        self._bastion_tunnel_proc = proc
        self._bastion_local_port = local_port
        self._bastion_started = True

        # Redirect the inherited ssh plugin at the loopback tunnel endpoint.
        # Assign directly into ``self._options`` (rather than calling
        # ``self.set_option``) because ``set_option`` validates against
        # OUR plugin's option spec, which doesn't define ``host``/``port``
        # (those come from the ``ssh`` plugin and are merged into
        # ``self._options`` by our ``set_options`` override).
        self._options["host"] = "127.0.0.1"
        self._options["port"] = local_port
        self.host = "127.0.0.1"
        self.port = local_port
        try:
            if self._play_context is not None:
                self._play_context.remote_addr = "127.0.0.1"
                self._play_context.port = local_port
        except AttributeError:
            pass

    def _teardown_tunnel(self):
        proc = self._bastion_tunnel_proc
        self._bastion_tunnel_proc = None
        self._bastion_local_port = None
        self._bastion_started = False
        if proc is None:
            return
        try:
            terminate_tunnel(proc)
        except Exception as exc:
            display.warning(
                "azure_bastion_ssh: failed to cleanly terminate tunnel "
                "(pid=%s): %s" % (getattr(proc, 'pid', '?'), exc)
            )
        finally:
            with _LIVE_TUNNELS_LOCK:
                _LIVE_TUNNELS.discard(proc)

    # -- connection plugin overrides --------------------------------------

    def _connect(self):
        self._ensure_tunnel()
        return super(Connection, self)._connect()

    def exec_command(self, cmd, in_data=None, sudoable=True):
        self._ensure_tunnel()
        return super(Connection, self).exec_command(cmd, in_data=in_data, sudoable=sudoable)

    def put_file(self, in_path, out_path):
        self._ensure_tunnel()
        return super(Connection, self).put_file(in_path, out_path)

    def fetch_file(self, in_path, out_path):
        self._ensure_tunnel()
        return super(Connection, self).fetch_file(in_path, out_path)

    def close(self):
        try:
            super(Connection, self).close()
        finally:
            self._teardown_tunnel()

    def reset(self):
        # Delegate to the parent which performs ControlPersist teardown via
        # ``ssh -O stop``. The parent reset ends by calling ``self.close()``,
        # so our override of ``close`` will tear down the tunnel as well.
        self._ensure_tunnel()
        return super(Connection, self).reset()
