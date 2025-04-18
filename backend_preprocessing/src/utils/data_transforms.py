import json

def get_nested(data, path):
    keys = path.split('.') if path else []
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key)
        elif isinstance(data, list) and key.isdigit():
            data = data[int(key)] if int(key) < len(data) else None
        else:
            return None
        if data is None:
            return None
    return data

def apply_mapping(data, mapping_spec):
    if isinstance(mapping_spec, str):
        return get_nested(data, mapping_spec)
    if isinstance(mapping_spec, dict):
        return {key: apply_mapping(data, spec) for key, spec in mapping_spec.items()}
    return None

def transform_log(input_data, mapping_spec):
    output_data = {"conversations": []}
    if isinstance(input_data, dict):
        input_data = [input_data]
    elif not isinstance(input_data, list):
        return output_data

    for conversation in input_data:
        transformed_conv = {}
        for out_field, spec in mapping_spec.items():
            if out_field not in ["messages", "message"]:
                transformed_conv[out_field] = apply_mapping(conversation, spec)

        messages_path = mapping_spec.get("messages", "")
        msgs = get_nested(conversation, messages_path) if messages_path else conversation
        if not isinstance(msgs, list):
            msgs = [msgs] if msgs is not None else []

        transformed_messages = []
        for msg in msgs:
            transformed_msg = apply_mapping(msg, mapping_spec["message"])
            transformed_messages.append(transformed_msg)
        transformed_conv["messages"] = transformed_messages
        output_data["conversations"].append(transformed_conv)
    return output_data

def group_flat_messages(input_data, mapping_spec):
    sessions = {}
    for item in input_data:
        mapped_msg = apply_mapping(item, mapping_spec["message"])
        session_id = item.get("session_id")
        user_id = item.get("user_id")
        if session_id not in sessions:
            sessions[session_id] = {
                "session_id": session_id,
                "user_id": user_id,
                "messages": []
            }
        sessions[session_id]["messages"].append(mapped_msg)
    return {"conversations": list(sessions.values())}

def create_interactions(transformed_data):
    interactions_output = []
    for conv in transformed_data.get("conversations", []):
        session_id = conv.get("session_id")
        user_id = conv.get("user_id")
        msgs = conv.get("messages", [])
        for i in range(0, len(msgs), 2):
            pair = msgs[i:i+2]
            bot_msg = None
            for m in pair:
                if m.get("sender", "").upper() == "BOT":
                    bot_msg = m
            if not bot_msg and pair:
                bot_msg = pair[0]
            simple_msgs = [{"role": m.get("sender"), "message": m.get("text")} for m in pair]
            interaction_id = bot_msg.get("id") if bot_msg and bot_msg.get("id") else f"{session_id}_{i//2+1}"
            interactions_output.append({
                "interaction_id": interaction_id,
                "interactions": json.dumps(simple_msgs),
                "session_id": session_id,
                "timestamp": bot_msg.get("timestamp") if bot_msg else None,
                "user_id": user_id,
                "ip_address": bot_msg.get("ip_address") if bot_msg else None,
                "agent_id": bot_msg.get("bot_id") if bot_msg else None,
                "agent_name": bot_msg.get("bot_name") if bot_msg else None
            })
    return interactions_output