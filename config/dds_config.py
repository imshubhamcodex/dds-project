import rti.connextdds as dds
import rti.types as idl

# Define message types for topics
@idl.struct
class FloatWrapper:
    value: float = 0.0

@idl.struct
class StringWrapper:
    content: str = ""

governance_file = "./governance.xml"

# Create a secure domain participant
def create_participant(domain_id=0):
    security_qos = dds.DomainParticipantQos()
    security_qos << dds.Property(
        {
            "dds.sec.access.governance": governance_file
        }
    )
    return dds.DomainParticipant(domain_id=domain_id, qos=security_qos)
