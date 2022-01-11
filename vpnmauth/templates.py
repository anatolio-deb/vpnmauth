from typing import Dict

PORT_NON_443: Dict = {
    "outbounds": [
        {
            "mux": {},
            "protocol": "vmess",
            "sendThrough": "0.0.0.0",
            "settings": {
                "vnext": [
                    {
                        "address": "",
                        "port": 80,
                        "users": [
                            {
                                "alterId": 0,
                                "id": "",
                                "level": 0,
                                "security": "auto",
                            }
                        ],
                    }
                ]
            },
            "streamSettings": {
                "dsSettings": {"path": "/"},
                "httpSettings": {"host": [], "path": "/"},
                "kcpSettings": {
                    "congestion": False,
                    "downlinkCapacity": 20,
                    "header": {"type": "none"},
                    "mtu": 1350,
                    "readBufferSize": 1,
                    "tti": 20,
                    "uplinkCapacity": 5,
                    "writeBufferSize": 1,
                },
                "network": "tcp",
                "quicSettings": {"header": {"type": "none"}, "key": "", "security": ""},
                "security": "",
                "sockopt": {"mark": 0, "tcpFastOpen": False, "tproxy": "off"},
                "tcpSettings": {
                    "header": {
                        "request": {
                            "headers": {},
                            "method": "GET",
                            "path": [],
                            "version": "1.1",
                        },
                        "response": {
                            "headers": {},
                            "reason": "OK",
                            "status": "200",
                            "version": "1.1",
                        },
                        "type": "none",
                    }
                },
                "tlsSettings": {
                    "allowInsecure": False,
                    "alpn": [],
                    "certificates": [],
                    "disableSystemRoot": False,
                    "serverName": "",
                },
                "wsSettings": {"headers": {}, "path": "/"},
            },
            "tag": "outBound_PROXY",
        }
    ]
}

PORT_443: Dict = {
    "outbounds": [
        {
            "mux": {},
            "protocol": "vmess",
            "sendThrough": "0.0.0.0",
            "settings": {
                "vnext": [
                    {
                        "address": "",
                        "port": 443,
                        "users": [
                            {
                                "alterId": 0,
                                "id": "",
                                "level": 0,
                                "security": "auto",
                            }
                        ],
                    }
                ]
            },
            "streamSettings": {
                "dsSettings": {"path": "/"},
                "httpSettings": {"host": [], "path": "/"},
                "kcpSettings": {
                    "congestion": False,
                    "downlinkCapacity": 20,
                    "header": {"type": "none"},
                    "mtu": 1350,
                    "readBufferSize": 1,
                    "tti": 20,
                    "uplinkCapacity": 5,
                    "writeBufferSize": 1,
                },
                "network": "ws",
                "quicSettings": {"header": {"type": "none"}, "key": "", "security": ""},
                "security": "tls",
                "sockopt": {"mark": 0, "tcpFastOpen": False, "tproxy": "off"},
                "tcpSettings": {
                    "header": {
                        "request": {
                            "headers": {},
                            "method": "GET",
                            "path": [],
                            "version": "1.1",
                        },
                        "response": {
                            "headers": {},
                            "reason": "OK",
                            "status": "200",
                            "version": "1.1",
                        },
                        "type": "none",
                    }
                },
                "tlsSettings": {
                    "allowInsecure": False,
                    "alpn": [],
                    "certificates": [],
                    "disableSystemRoot": False,
                    "serverName": "",
                },
                "wsSettings": {
                    "headers": {"Host": "red-blue-01.online"},
                    "path": "/download",
                },
            },
            "tag": "outBound_PROXY",
        }
    ]
}
