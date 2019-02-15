conversation_seed = [
    {
        "sender_id": 1,
        "receiver_id": 2,
        "content": "test message"
    },
    {
        "sender_id": 2,
        "receiver_id": 1,
        "content": "test reply"
    }
]

conversation_request = [
    {
        "content":"test message",
        "id":1,
        "sender_id":1
    },
    {
        "content":"test reply",
        "id":2,
        "sender_id":2
    }
]

latest_conversations_seed = [
    {
        "sender_id": 1,
        "receiver_ids": [
                2
            ],
        "content": "test message"
    },
    {
        "sender_id": 1,
        "receiver_ids": [
                3
            ],
        "content": "test message"
    },
    {
        "sender_id": 1,
        "receiver_ids": [
                4
            ],
        "content": "test message"
    },
    {
        "sender_id": 1,
        "receiver_ids": [
                5
            ],
        "content": "test message"
    },
    {
        "sender_id": 1,
        "receiver_ids": [
                6
            ],
        "content": "test message"
    }
]

latest_conversations_response = [
    {
        "conversation_id": 1,
        "participant_ids": [
                2
            ],
        "last_message": "test message"
    },
    {
        "conversation_id": 2,
        "participant_ids": [
                3
            ],
        "last_message": "test message"
    },
    {
        "conversation_id": 3,
        "participant_ids": [
                4
            ],
        "last_message": "test message"
    },
    {
        "conversation_id": 4,
        "participant_ids": [
                5
            ],
        "last_message": "test message"
    },
    {
        "conversation_id": 5,
        "participant_ids": [
                6
            ],
        "last_message": "test message"
    }
]

valid_json_message = { 
    "content": "test message",
    "sender_id": 1,
    "receiver_ids": [
        2
    ]
}

invalid_json_message = { 
    "content": None,
    "sender_id": 1,
    "receiver_ids": [
        2
    ]
}

create_message_response = {
    "succeeded": {
        "saved": True
    },
    "failed": {
        "saved": False,
        'error': 'null value in column "content" violates not-null constraint'
    }
}