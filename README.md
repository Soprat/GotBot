# GotBot
Bot allows to copy data and messages from channel to channel.

---
## Commands:
1. ```/merge --d <donors> --t <targets> --del <text_to_del> --set <texts_to_set>```
   - > Creates a database cluster and starts to send messages from \<donors> to \<targets>, with replacing <text_to_del> on <text_to_set>.
   - > Flags can be placed in any order you want.
   - > You can skip <text_to_del> and <text_to_set>
2. ```/change_text --d <donor> --del <text_to_del> --set <text_to_set>```
   - > Changes <text_to_del> and <text_to_set> in cluster, where \<donor> in cluster.
   - > Flags can be placed in any order you want.
3. ```/cluster_info <donor>```
   - > Replies with all cluster info, where \<donor> in cluster.
4. ```/chat_id```
   - > Should be an answer on message, forwarded from chat.
   - > Answers with id of chat, message forwarded from.
