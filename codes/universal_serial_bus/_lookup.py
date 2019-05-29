endpoint_direction = {0x80: "In", 0x00: "Out"}

endpoint_transfer_types = {0x0: "Control",
                           0x1: "Isochronous",
                           0x2: "Bulk",
                           0x3: "Interrupt"}

endpoint_synchronization_types = {0x0: "No_Synchronization",
                                  0x1: "Asynchronous",
                                  0x2: "Adaptive",
                                  0x3: "Synchronous"}

endpoint_usage_types = {0x0: "Data_endpoint",
                        0x1: "Feedback_endpoint",
                        0x2: "Implicit_feedback_Data_endpoint",
                        0x3: "Reserved"}
