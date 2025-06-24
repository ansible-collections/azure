
# How to Configure EDA to use Azure servicebus as a source

## First - See the Ansible Rulebook Documentation

Documentation about Ansbile Rulebooks and EDA are available [here](https://ansible.readthedocs.io/projects/rulebook/en/latest/).  See the Getting started and Installation sections before continuing.

## Example azure-rulebook.yml file:

```yaml
---
- name: Listen for events from azure
  hosts: all
  sources:
    - azure.azcollection.azure_service_bus:
        conn_str: **CONNECTION_STRING**
        queue_name: **QUEUE_NAME**
  rules:
    - name: Say Hello
      condition: event.body.message == "Azure and Ansible is super cool"
      action:
        run_playbook:
          name: hello_playbook.yml
```

Rulebooks are run via ansible-rulebook or from AAP:

    ansible-rulebook -r azure-rulebook.yml -v -i inventory

## Here is a crude example of sending a message to servicebus with python:

```python
import os
import threading
import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage


CONNECTION_STRING = os.environ["SERVICEBUS_CONNECTION_STRING"]
QUEUE_NAME = os.environ["SERVICEBUS_QUEUE_NAME"]


def send_single_message(sender, data):
    message = ServiceBusMessage(json.dumps(data))
    sender.send_messages(message)


servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STRING,
                                                            logging_enable=True)
data = dict(message="Azure and Ansible is super cool")
with servicebus_client:
    sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
    with sender:
        send_single_message(sender, data)

    print("Send message is done.")
```

## Example debug output from running the above rulebook and receiving the example message

```
2025-06-23 14:46:44,667 - azure.servicebus._pyamqp.receiver - DEBUG - <- TransferFrame(handle=2, delivery_id=1, delivery_tag=b'5\x14\xda\xf8\xe7CKN\xa3\x0b\x9a\x16yx\xe5\xa2', message_format=0, settled=None, more=False, rcv_settle_mode=None, state=None, resume=None, aborted=None, batchable=True, payload=b'***')
2025-06-23 14:46:44,667 - azure.servicebus._transport._pyamqp_transport - DEBUG - Received message: seq-num: 15, enqd-utc: datetime.datetime(2025, 6, 23, 18, 46, 44, 637000, tzinfo=datetime.timezone.utc), lockd-til-utc: datetime.datetime(2025, 6, 23, 18, 47, 44, 652000, tzinfo=datetime.timezone.utc), ttl: datetime.timedelta(days=14), dlvry-cnt: 0
2025-06-23 14:46:44,667 - azure.servicebus._pyamqp.receiver - DEBUG - -> DispositionFrame(role=True, first=1, last=None, settled=True, state=Accepted(), batchable=None)

** 2025-06-23 14:46:44.668293 [received event] **********************************************************************
2025-06-23 14:46:44,668 - azure.servicebus._pyamqp.cbs - DEBUG - CBS status check: state == <CbsAuthState.OK: 0>, expired == False, refresh required == False
Ruleset: Listen for events from azure
2025-06-23 14:46:44,668 - azure.servicebus._pyamqp.session - DEBUG - -> FlowFrame(next_incoming_id=3, incoming_window=65534, next_outgoing_id=1, outgoing_window=65535, handle=3, delivery_count=1, link_credit=1, available=None, drain=None, echo=None, properties=None)
Event:
{'body': {'message': 'Azure and Ansible is super cool'},
 'meta': {'message_id': '80a59815-3c23-41f2-9889-9893a4b9c2da',
          'received_at': '2025-06-23T18:46:44.668093Z',
          'source': {'name': 'azure.azcollection.azure_service_bus',
                     'type': 'azure.azcollection.azure_service_bus'},
          'uuid': '07f5c3b7-ebf5-4204-9151-864e44a4829e'}}
*********************************************************************************************************************
2025-06-23 14:46:44,668 - ansible_rulebook.rule_set_runner - DEBUG - Posting data to ruleset Listen for events from azure => {'body': {'message': 'Azure and Ansible is super cool'}, 'meta': {'message_id': '80a59815-3c23-41f2-9889-9893a4b9c2da', 'source': {'name': 'azure.azcollection.azure_service_bus', 'type': 'azure.azcollection.azure_service_bus'}, 'received_at': '2025-06-23T18:46:44.668093Z', 'uuid': '07f5c3b7-ebf5-4204-9151-864e44a4829e'}}
2025-06-23 14:46:44 669 [main] INFO org.drools.ansible.rulebook.integration.api.rulesengine.MemoryMonitorUtil - Memory occupation threshold set to 90%
2025-06-23 14:46:44 670 [main] INFO org.drools.ansible.rulebook.integration.api.rulesengine.MemoryMonitorUtil - Memory check event count threshold set to 64
2025-06-23 14:46:44 670 [main] INFO org.drools.ansible.rulebook.integration.api.rulesengine.MemoryMonitorUtil - Exit above memory occupation threshold set to false
2025-06-23 14:46:44 711 [main] DEBUG org.drools.ansible.rulebook.integration.api.rulesengine.RegisterOnlyAgendaFilter - Activation of effective rule "Say Hello" with facts: {m={meta={message_id=80a59815-3c23-41f2-9889-9893a4b9c2da, source={name=azure.azcollection.azure_service_bus, type=azure.azcollection.azure_service_bus}, received_at=2025-06-23T18:46:44.668093Z, uuid=07f5c3b7-ebf5-4204-9151-864e44a4829e}, body={message=Azure and Ansible is super cool}}}
2025-06-23 14:46:44,718 - drools.ruleset - DEBUG - Calling rule : Say Hello in session: 1
2025-06-23 14:46:44,718 - ansible_rulebook.rule_generator - DEBUG - callback calling Say Hello
2025-06-23 14:46:44,718 - ansible_rulebook.rule_set_runner - DEBUG - None
2025-06-23 14:46:44,718 - ansible_rulebook.rule_set_runner - DEBUG - Creating action task action::run_playbook::Listen for events from azure::Say Hello
2025-06-23 14:46:44,718 - ansible_rulebook.rule_set_runner - DEBUG - call_action run_playbook
2025-06-23 14:46:44,719 - ansible_rulebook.action.run_playbook - DEBUG - ruleset: Listen for events from azure, rule: Say Hello
2025-06-23 14:46:44,719 - ansible_rulebook.action.run_playbook - DEBUG - private data dir /tmp/edap29wpkf2
2025-06-23 14:46:44,721 - ansible_rulebook.action.run_playbook - DEBUG - project_data_file: None
```
