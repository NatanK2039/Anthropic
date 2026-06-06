from UserInterfaceRebuild import create_ui
from ConversationRebuild import conversation
from LoggerRebuild1 import log
from Ingester import on_file_drop

log("------------- New Conversation -------------")
create_ui(conversation, on_file_drop)

