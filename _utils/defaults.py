# -*- coding: utf-8 -*-
# Authors: Kruthika Rathinavel
# Version: 1.2.1
# Email: kruthika@vt.edu
# Created: "2014-10-13 18:45:40"
# Updated: "2015-02-13 15:06:41"


# Copyright © 2014 by Virginia Polytechnic Institute and State University
# All rights reserved
#
# Virginia Polytechnic Institute and State University (Virginia Tech) owns the copyright for the BEMOSS software and its
# associated documentation ("Software") and retains rights to grant research rights under patents related to
# the BEMOSS software to other academic institutions or non-profit research institutions.
# You should carefully read the following terms and conditions before using this software.
# Your use of this Software indicates your acceptance of this license agreement and all terms and conditions.
#
# You are hereby licensed to use the Software for Non-Commercial Purpose only.  Non-Commercial Purpose means the
# use of the Software solely for research.  Non-Commercial Purpose excludes, without limitation, any use of
# the Software, as part of, or in any way in connection with a product or service which is sold, offered for sale,
# licensed, leased, loaned, or rented.  Permission to use, copy, modify, and distribute this compilation
# for Non-Commercial Purpose to other academic institutions or non-profit research institutions is hereby granted
# without fee, subject to the following terms of this license.
#
# Commercial Use: If you desire to use the software for profit-making or commercial purposes,
# you agree to negotiate in good faith a license with Virginia Tech prior to such profit-making or commercial use.
# Virginia Tech shall have no obligation to grant such license to you, and may grant exclusive or non-exclusive
# licenses to others. You may contact the following by email to discuss commercial use:: vtippatents@vtip.org
#
# Limitation of Liability: IN NO EVENT WILL VIRGINIA TECH, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR REDISTRIBUTE
# THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR
# CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO
# LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE
# OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF VIRGINIA TECH OR OTHER PARTY HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGES.
#
# For full terms and conditions, please visit https://bitbucket.org/bemoss/bemoss_os.
#
# Address all correspondence regarding this license to Virginia Tech's electronic mail address: vtippatents@vtip.org

__author__ = 'kruthika'

DISABLED_VALUES_THERMOSTAT = {"everyday": {
            'monday_heat': [],
            'monday_cool': [],
            'tuesday_heat': [],
            'tuesday_cool': [],
            'wednesday_heat': [],
            'wednesday_cool': [],
            'thursday_heat': [],
            'thursday_cool': [],
            'friday_heat': [],
            'friday_cool': [],
            'saturday_heat': [],
            'saturday_cool': [],
            'sunday_heat': [],
            'sunday_cool': []},
        "weekdayweekend": {
            'weekday_heat': [],
            'weekday_cool': [],
            'weekend_heat': [],
            'weekend_cool': []},
        "holiday": {
            'holiday_heat': [],
            'holiday_cool': [],
        }}

DISABLED_VALUES_LIGHTING = {"everyday": {
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': [],
            'sunday': []},
        "weekdayweekend": {
            'weekday': [],
            'weekend': []},
        "holiday": {
            'holiday': []}}

DISABLED_VALUES_PLUGLOAD = {"everyday": {
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': [],
            'sunday': []},
        "weekdayweekend": {
            'weekday': [],
            'weekend': []},
        "holiday": {
            'holiday': []}}

THERMOSTAT_DEFAULT_SCHEDULE = {
                "everyday": {
                    "friday": {
                        "cool": [
                            {
                                "at": "420",
                                "id": "1",
                                "nickname": "Period1",
                                "setpoint": "72"
                            },
                            {
                                "at": "1140",
                                "id": "2",
                                "nickname": "Period2",
                                "setpoint": "80"
                            }
                        ],
                        "heat": [
                            {
                                "at": "420",
                                "id": "1",
                                "nickname": "Period1",
                                "setpoint": "72"
                            },
                            {
                                "at": "1140",
                                "id": "2",
                                "nickname": "Period2",
                                "setpoint": "65"
                            }
                        ]
                    },
                    "monday": {
                        "cool": [
                            {
                                "at": "420",
                                "id": "1",
                                "nickname": "Period1",
                                "setpoint": "72"
                            },
                            {
                                "at": "1140",
                                "id": "2",
                                "nickname": "Period2",
                                "setpoint": "80"
                            }
                        ],
                        "heat": [
                            {
                                "at": "420",
                                "id": "1",
                                "nickname": "Period1",
                                "setpoint": "72"
                            },
                            {
                                "at": "1140",
                                "id": "2",
                                "nickname": "Period2",
                                "setpoint": "65"
                            }
                        ]
                    },
                    "saturday": {
                        "cool": [
                            {
                                "at": "420",
                                "id": "1",
                                "nickname": "Period1",
                                "setpoint": "72"
                            },
                            {
                                "at": "1140",
                                "id": "2",
                                "nickname": "Period2",
                                "setpoint": "80"
                            }
                        ],
                        "heat": [
                            {
                                "at": "420",
                                "id": "1",
                                "nickname": "Period1",
                                "setpoint": "72"
                            },
                            {
                                "at": "1140",
                                "id": "2",
                                "nickname": "Period2",
                                "setpoint": "65"
                            }
                        ]
                    },
                    "sunday": {
                        "cool": [
                            {
                                "at": "420",
                                "id": "1",
                                "nickname": "Period1",
                                "setpoint": "72"
                            },
                            {
                                "at": "1140",
                                "id": "2",
                                "nickname": "Period2",
                                "setpoint": "80"
                            }
                        ],
                        "heat": [
                            {
                                "at": "420",
                                "id": "1",
                                "nickname": "Period1",
                                "setpoint": "72"
                            },
                            {
                                "at": "1140",
                                "id": "2",
                                "nickname": "Period2",
                                "setpoint": "65"
                            }
                        ]
                    },
                    "thursday": {
                        "cool": [
                            {
                                "at": "420",
                                "id": "1",
                                "nickname": "Period1",
                                "setpoint": "72"
                            },
                            {
                                "at": "1140",
                                "id": "2",
                                "nickname": "Period2",
                                "setpoint": "80"
                            }
                        ],
                        "heat": [
                            {
                                "at": "420",
                                "id": "1",
                                "nickname": "Period1",
                                "setpoint": "72"
                            },
                            {
                                "at": "1140",
                                "id": "2",
                                "nickname": "Period2",
                                "setpoint": "65"
                            }
                        ]
                    },
                    "tuesday": {
                        "cool": [
                            {
                                "at": "420",
                                "id": "1",
                                "nickname": "Period1",
                                "setpoint": "72"
                            },
                            {
                                "at": "30",
                                "id": "2",
                                "nickname": "Period2",
                                "setpoint": "80"
                            }
                        ],
                        "heat": [
                            {
                                "at": "420",
                                "id": "1",
                                "nickname": "Period1",
                                "setpoint": "72"
                            },
                            {
                                "at": "1140",
                                "id": "2",
                                "nickname": "Period2",
                                "setpoint": "65"
                            }
                        ]
                    },
                    "wednesday": {
                        "cool": [
                            {
                                "at": "420",
                                "id": "1",
                                "nickname": "Period1",
                                "setpoint": "72"
                            },
                            {
                                "at": "1140",
                                "id": "2",
                                "nickname": "Period2",
                                "setpoint": "80"
                            }
                        ],
                        "heat": [
                            {
                                "at": "420",
                                "id": "1",
                                "nickname": "Period1",
                                "setpoint": "72"
                            },
                            {
                                "at": "1140",
                                "id": "2",
                                "nickname": "Period2",
                                "setpoint": "65"
                            }
                        ]
                    }
                },
                "holiday": {
                    "cool": [
                        {
                            "at": "420",
                            "id": "1",
                            "nickname": "Period1",
                            "setpoint": "72"
                        },
                        {
                            "at": "1140",
                            "id": "2",
                            "nickname": "Period2",
                            "setpoint": "80"
                        }
                    ],
                    "heat": [
                        {
                            "at": "420",
                            "id": "1",
                            "nickname": "Period1",
                            "setpoint": "72"
                        },
                        {
                            "at": "1140",
                            "id": "2",
                            "nickname": "Period2",
                            "setpoint": "65"
                        }
                    ]
                }
            }

LIGHTING_DEFAULT_SCHEDULE_2HUE = {
                "everyday": {
                    "friday": [
                        {
                            "at": 420,
                            "brightness": 100,
                            "color": "(255, 255, 255)",
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "brightness": 0,
                            "color": "(255, 255, 255)",
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "monday": [
                        {
                            "at": 420,
                            "brightness": 100,
                            "color": "(255, 255, 255)",
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "brightness": 0,
                            "color": "(255, 255, 255)",
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "saturday": [
                        {
                            "at": 420,
                            "brightness": 100,
                            "color": "(255, 255, 255)",
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "brightness": 0,
                            "color": "(255, 255, 255)",
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "sunday": [
                        {
                            "at": 420,
                            "brightness": 100,
                            "color": "(255, 255, 255)",
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "brightness": 0,
                            "color": "(255, 255, 255)",
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "thursday": [
                        {
                            "at": 420,
                            "brightness": 100,
                            "color": "(255, 255, 255)",
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "brightness": 0,
                            "color": "(255, 255, 255)",
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "tuesday": [
                        {
                            "at": 420,
                            "brightness": 100,
                            "color": "(255, 255, 255)",
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "brightness": 0,
                            "color": "(255, 255, 255)",
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "wednesday": [
                        {
                            "at": 420,
                            "brightness": 100,
                            "color": "(255, 255, 255)",
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "brightness": 0,
                            "color": "(255, 255, 255)",
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ]
                },
                "holiday": {
                    "holiday": [
                        {
                            "at": 420,
                            "brightness": 100,
                            "color": "(255, 255, 255)",
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "brightness": 0,
                            "color": "(255, 255, 255)",
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ]
                }
            }

LIGHTING_DEFAULT_SCHEDULE_2DB_2SDB = {
                "everyday": {
                    "friday": [
                        {
                            "at": 420,
                            "brightness": 100,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "brightness": 0,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "monday": [
                        {
                            "at": 420,
                            "brightness": 100,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "brightness": 0,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "saturday": [
                        {
                            "at": 420,
                            "brightness": 100,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "brightness": 0,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "sunday": [
                        {
                            "at": 420,
                            "brightness": 100,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "brightness": 0,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "thursday": [
                        {
                            "at": 420,
                            "brightness": 100,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "brightness": 0,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "tuesday": [
                        {
                            "at": 420,
                            "brightness": 100,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "brightness": 0,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "wednesday": [
                        {
                            "at": 420,
                            "brightness": 100,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "brightness": 0,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ]
                },
                "holiday": {
                    "holiday": [
                        {
                            "at": 420,
                            "brightness": 100,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "brightness": 0,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ]
                }
            }

LIGHTING_DEFAULT_SCHEDULE_2WL = {
                "everyday": {
                    "friday": [
                        {
                            "at": 420,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "monday": [
                        {
                            "at": 420,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "saturday": [
                        {
                            "at": 420,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "sunday": [
                        {
                            "at": 420,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "thursday": [
                        {
                            "at": 420,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "tuesday": [
                        {
                            "at": 420,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "wednesday": [
                        {
                            "at": 420,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ]
                },
                "holiday": {
                    "holiday": [
                        {
                            "at": 420,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ]
                }
            }

PLUGLOAD_DEFAULT_SCHEDULE = {
                "everyday": {
                    "friday": [
                        {
                            "at": 420,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "monday": [
                        {
                            "at": 420,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "saturday": [
                        {
                            "at": 420,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "sunday": [
                        {
                            "at": 420,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "thursday": [
                        {
                            "at": 420,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "tuesday": [
                        {
                            "at": 420,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ],
                    "wednesday": [
                        {
                            "at": 420,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ]
                },
                "holiday": {
                    "holiday": [
                        {
                            "at": 420,
                            "id": "1",
                            "nickname": "Period1",
                            "status": "ON"
                        },
                        {
                            "at": 1140,
                            "id": "2",
                            "nickname": "Period2",
                            "status": "OFF"
                        }
                    ]
                }
            }