CLASS_RULE_PARAM_VALIDATION = [
   {
      "class": "PaymentPlan",
      "parameters": [
         {
            "type": "select",
            "name": "claim_type",
            "label": {
               "en": "claim type",
               "fr": "Type de prestation"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "B",
                  "label": {
                     "en": "All",
                     "fr": "toutes"
                  }
               },
               {
                  "value": "I",
                  "label": {
                     "en": "Hospital/in-patient",
                     "fr": "Hopital"
                  }
               },
               {
                  "value": "O",
                  "label": {
                     "en": "None-Hospital/out-patient",
                     "fr": "Hors hopitaux"
                  }
               }
            ]
         },
         {
            "type": "select",
            "name": "hf_level_1",
            "label": {
               "en": "Level 1",
               "fr": "Niveau 1"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "null",
                  "label": {
                     "en": "",
                     "fr": ""
                  }
               },
               {
                  "value": "H",
                  "label": {
                     "en": "Hospital",
                     "fr": "Hopital"
                  }
               },
               {
                  "value": "D",
                  "label": {
                     "en": "Dispensary",
                     "fr": "Dispensaire"
                  }
               },
               {
                  "value": "C",
                  "label": {
                     "en": "Health center",
                     "fr": "Centre de santé"
                  }
               }
            ],
            "default": "null"
         },
         {
            "type": "select",
            "name": "hf_sublevel_1",
            "label": {
               "en": "Sublevel 1",
               "fr": "Sublevel 1"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "null",
                  "label": {
                     "en": "",
                     "fr": ""
                  }
               },
               {
                  "value": "D",
                  "label": {
                     "en": "District",
                     "fr": "District"
                  }
               },
               {
                  "value": "R",
                  "label": {
                     "en": "Region",
                     "fr": "Region"
                  }
               }
            ],
            "default": "null"
         },
         {
            "type": "select",
            "name": "hf_level_2",
            "label": {
               "en": "Level 2",
               "fr": "Niveau 2"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "null",
                  "label": {
                     "en": "",
                     "fr": ""
                  }
               },
               {
                  "value": "H",
                  "label": {
                     "en": "Hospital",
                     "fr": "Hopital"
                  }
               },
               {
                  "value": "D",
                  "label": {
                     "en": "Dispensary",
                     "fr": "Dispensaire"
                  }
               },
               {
                  "value": "C",
                  "label": {
                     "en": "Health center",
                     "fr": "Centre de santé"
                  }
               }
            ],
            "default": "null"
         },
         {
            "type": "select",
            "name": "hf_sublevel_2",
            "label": {
               "en": "Sublevel 2",
               "fr": "Sublevel 2"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "null",
                  "label": {
                     "en": "",
                     "fr": ""
                  }
               },
               {
                  "value": "D",
                  "label": {
                     "en": "District",
                     "fr": "District"
                  }
               },
               {
                  "value": "R",
                  "label": {
                     "en": "Region",
                     "fr": "Region"
                  }
               }
            ],
            "default": "null"
         },
         {
            "type": "select",
            "name": "hf_level_3",
            "label": {
               "en": "Level 3",
               "fr": "Niveau 3"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "null",
                  "label": {
                     "en": "",
                     "fr": ""
                  }
               },
               {
                  "value": "H",
                  "label": {
                     "en": "Hospital",
                     "fr": "Hopital"
                  }
               },
               {
                  "value": "D",
                  "label": {
                     "en": "Dispensary",
                     "fr": "Dispensaire"
                  }
               },
               {
                  "value": "C",
                  "label": {
                     "en": "Health center",
                     "fr": "Centre de santé"
                  }
               }
            ],
            "default": "null"
         },
         {
            "type": "select",
            "name": "hf_sublevel_3",
            "label": {
               "en": "Sublevel 3",
               "fr": "Sublevel 3"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "null",
                  "label": {
                     "en": "",
                     "fr": ""
                  }
               },
               {
                  "value": "D",
                  "label": {
                     "en": "District",
                     "fr": "District"
                  }
               },
               {
                  "value": "R",
                  "label": {
                     "en": "Region",
                     "fr": "Region"
                  }
               }
            ],
            "default": "null"
         },
         {
            "type": "select",
            "name": "hf_level_4",
            "label": {
               "en": "Level 4",
               "fr": "Niveau 4"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "null",
                  "label": {
                     "en": "",
                     "fr": ""
                  }
               },
               {
                  "value": "H",
                  "label": {
                     "en": "Hospital",
                     "fr": "Hopital"
                  }
               },
               {
                  "value": "D",
                  "label": {
                     "en": "Dispensary",
                     "fr": "Dispensaire"
                  }
               },
               {
                  "value": "C",
                  "label": {
                     "en": "Health center",
                     "fr": "Centre de santé"
                  }
               }
            ],
            "default": "null"
         },
         {
            "type": "select",
            "name": "hf_sublevel_4",
            "label": {
               "en": "Sublevel 4",
               "fr": "Sublevel 4"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "null",
                  "label": {
                     "en": "",
                     "fr": ""
                  }
               },
               {
                  "value": "D",
                  "label": {
                     "en": "District",
                     "fr": "District"
                  }
               },
               {
                  "value": "R",
                  "label": {
                     "en": "Region",
                     "fr": "Region"
                  }
               }
            ],
            "default": "null"
         },
         {
            "type": "number",
            "name": "share_contribution",
            "label": {
               "en": "Share Contribution",
               "fr": "Share Contribution"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "condition": "INPUT<100",
            "default": ""
         },
         {
            "type": "number",
            "name": "weight_population",
            "label": {
               "en": "Weight Population",
               "fr": "Weight Population"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "condition": "INPUT<100",
            "default": ""
         },
         {
            "type": "number",
            "name": "weight_number_families",
            "label": {
               "en": "Weight Number Families",
               "fr": "Weight Number Families"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "condition": "INPUT<100",
            "default": ""
         },
         {
            "type": "number",
            "name": "weight_insured_population",
            "label": {
               "en": "Weight of Insured Population",
               "fr": "Weight of Insured Population"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "condition": "INPUT<100",
            "default": ""
         },
         {
            "type": "number",
            "name": "weight_number_insured_families",
            "label": {
               "en": "Weight Number Insured Families",
               "fr": "Weight Number Insured Families"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "condition": "INPUT<100",
            "default": ""
         },
         {
            "type": "number",
            "name": "weight_number_visits",
            "label": {
               "en": "Weight Number Visits",
               "fr": "Weight Number Visits"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "condition": "INPUT<100",
            "default": ""
         },
         {
            "type": "number",
            "name": "weight_adjusted_amount",
            "label": {
               "en": "Weight Adjusted Amount",
               "fr": "Weight Adjusted Amount"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "condition": "INPUT<=100",
            "default": ""
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_1",
            "label": {
               "en": "distribution 1",
               "fr": "distribution 1"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(1, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_2",
            "label": {
               "en": "distribution 2",
               "fr": "distribution 2"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(2, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_3",
            "label": {
               "en": "distribution 3",
               "fr": "distribution 3"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(3, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_4",
            "label": {
               "en": "distribution 4",
               "fr": "distribution 4"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": " MOD(4, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_5",
            "label": {
               "en": "distribution 5",
               "fr": "distribution 5"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(5, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_6",
            "label": {
               "en": "distribution 6",
               "fr": "distribution 6"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(6, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_7",
            "label": {
               "en": "distribution 7",
               "fr": "distribution 7"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(7, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_8",
            "label": {
               "en": "distribution 8",
               "fr": "distribution 8"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(8, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_9",
            "label": {
               "en": "distribution 9",
               "fr": "distribution 9"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(9, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_10",
            "label": {
               "en": "distribution 10",
               "fr": "distribution 10"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(10, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_11",
            "label": {
               "en": "distribution 11",
               "fr": "distribution 11"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(11, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_12",
            "label": {
               "en": "distribution 12",
               "fr": "distribution 12"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(12, OBJECT.periodicity) = 0"
         }
      ]
   },
   {
      "class": "Product",
      "parameters": [
         {
            "type": "select",
            "name": "claim_type",
            "label": {
               "en": "claim type",
               "fr": "Type de prestation"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "B",
                  "label": {
                     "en": "All",
                     "fr": "toutes"
                  }
               },
               {
                  "value": "I",
                  "label": {
                     "en": "Hospital/in-patient",
                     "fr": "Hopital"
                  }
               },
               {
                  "value": "O",
                  "label": {
                     "en": "None-Hospital/out-patient",
                     "fr": "Hors hopitaux"
                  }
               }
            ]
         },
         {
            "type": "select",
            "name": "hf_level_1",
            "label": {
               "en": "Level 1",
               "fr": "Niveau 1"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "H",
                  "label": {
                     "en": "Hospital",
                     "fr": "Hopital"
                  }
               },
               {
                  "value": "D",
                  "label": {
                     "en": "Dispensary",
                     "fr": "Dispensaire"
                  }
               },
               {
                  "value": "C",
                  "label": {
                     "en": "Health center",
                     "fr": "Centre de santé"
                  }
               }
            ],
            "default": "null"
         },
         {
            "type": "select",
            "name": "hf_sublevel_1",
            "label": {
               "en": "Sublevel 1",
               "fr": "Sublevel 1"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "D",
                  "label": {
                     "en": "District",
                     "fr": "District"
                  }
               },
               {
                  "value": "R",
                  "label": {
                     "en": "Region",
                     "fr": "Region"
                  }
               }
            ],
            "default": "null"
         },
         {
            "type": "select",
            "name": "hf_level_2",
            "label": {
               "en": "Level 2",
               "fr": "Niveau 2"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "H",
                  "label": {
                     "en": "Hospital",
                     "fr": "Hopital"
                  }
               },
               {
                  "value": "D",
                  "label": {
                     "en": "Dispensary",
                     "fr": "Dispensaire"
                  }
               },
               {
                  "value": "C",
                  "label": {
                     "en": "Health center",
                     "fr": "Centre de santé"
                  }
               }
            ],
            "default": "null"
         },
         {
            "type": "select",
            "name": "hf_sublevel_2",
            "label": {
               "en": "Sublevel 2",
               "fr": "Sublevel 2"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "D",
                  "label": {
                     "en": "District",
                     "fr": "District"
                  }
               },
               {
                  "value": "R",
                  "label": {
                     "en": "Region",
                     "fr": "Region"
                  }
               }
            ],
            "default": "null"
         },
         {
            "type": "select",
            "name": "hf_level_3",
            "label": {
               "en": "Level 3",
               "fr": "Niveau 3"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "H",
                  "label": {
                     "en": "Hospital",
                     "fr": "Hopital"
                  }
               },
               {
                  "value": "D",
                  "label": {
                     "en": "Dispensary",
                     "fr": "Dispensaire"
                  }
               },
               {
                  "value": "C",
                  "label": {
                     "en": "Health center",
                     "fr": "Centre de santé"
                  }
               }
            ],
            "default": "null"
         },
         {
            "type": "select",
            "name": "hf_sublevel_3",
            "label": {
               "en": "Sublevel 3",
               "fr": "Sublevel 3"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "D",
                  "label": {
                     "en": "District",
                     "fr": "District"
                  }
               },
               {
                  "value": "R",
                  "label": {
                     "en": "Region",
                     "fr": "Region"
                  }
               }
            ],
            "default": "null"
         },
         {
            "type": "select",
            "name": "hf_level_4",
            "label": {
               "en": "Level 4",
               "fr": "Niveau 4"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "H",
                  "label": {
                     "en": "Hospital",
                     "fr": "Hopital"
                  }
               },
               {
                  "value": "D",
                  "label": {
                     "en": "Dispensary",
                     "fr": "Dispensaire"
                  }
               },
               {
                  "value": "C",
                  "label": {
                     "en": "Health center",
                     "fr": "Centre de santé"
                  }
               }
            ],
            "default": "null"
         },
         {
            "type": "select",
            "name": "hf_sublevel_4",
            "label": {
               "en": "Sublevel 4",
               "fr": "Sublevel 4"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "optionSet": [
               {
                  "value": "D",
                  "label": {
                     "en": "District",
                     "fr": "District"
                  }
               },
               {
                  "value": "R",
                  "label": {
                     "en": "Region",
                     "fr": "Region"
                  }
               }
            ],
            "default": "null"
         },
         {
            "type": "number",
            "name": "share_contribution",
            "label": {
               "en": "Share Contribution",
               "fr": "Share Contribution"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "condition": "INPUT<100",
            "default": ""
         },
         {
            "type": "number",
            "name": "weight_population",
            "label": {
               "en": "Weight Population",
               "fr": "Weight Population"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "condition": "INPUT<100",
            "default": ""
         },
         {
            "type": "number",
            "name": "weight_number_families",
            "label": {
               "en": "Weight Number Families",
               "fr": "Weight Number Families"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "condition": "INPUT<100",
            "default": ""
         },
         {
            "type": "number",
            "name": "weight_insured_population",
            "label": {
               "en": "Weight Number Population",
               "fr": "Weight Number Population"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "condition": "INPUT<100",
            "default": ""
         },
         {
            "type": "number",
            "name": "weight_number_insured_families",
            "label": {
               "en": "Weight Number Insured Families",
               "fr": "Weight Number Insured Families"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "condition": "INPUT<100",
            "default": ""
         },
         {
            "type": "number",
            "name": "weight_number_visits",
            "label": {
               "en": "Weight Number Visits",
               "fr": "Weight Number Visits"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "condition": "INPUT<100",
            "default": ""
         },
         {
            "type": "number",
            "name": "weight_adjusted_amount",
            "label": {
               "en": "Weight Adjusted Amount",
               "fr": "Weight Adjusted Amount"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "True",
            "condition": "INPUT<100",
            "default": ""
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_1",
            "label": {
               "en": "distribution 1",
               "fr": "distribution 1"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(1, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_2",
            "label": {
               "en": "distribution 2",
               "fr": "distribution 2"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(2, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_3",
            "label": {
               "en": "distribution 3",
               "fr": "distribution 3"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(3, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_4",
            "label": {
               "en": "distribution 4",
               "fr": "distribution 4"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": " MOD(4, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_5",
            "label": {
               "en": "distribution 5",
               "fr": "distribution 5"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(5, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_6",
            "label": {
               "en": "distribution 6",
               "fr": "distribution 6"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(6, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_7",
            "label": {
               "en": "distribution 7",
               "fr": "distribution 7"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(7, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_8",
            "label": {
               "en": "distribution 8",
               "fr": "distribution 8"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(8, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_9",
            "label": {
               "en": "distribution 9",
               "fr": "distribution 9"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(9, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_10",
            "label": {
               "en": "distribution 10",
               "fr": "distribution 10"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(10, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_11",
            "label": {
               "en": "distribution 11",
               "fr": "distribution 11"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(11, OBJECT.periodicity) = 0"
         },
         {
            "type": "number",
            "default": "0",
            "name": "distr_12",
            "label": {
               "en": "distribution 12",
               "fr": "distribution 12"
            },
            "rights": {
               "read": "121001",
               "write": "121002",
               "update": "121003",
               "replace": "121006"
            },
            "relevance": "MOD(12, OBJECT.periodicity) = 0"
         }
      ]
   }
]


FROM_TO = [
        {'from':  'BatchRun', 'to':  'Bill'},
        {'from':  'CapitationPayment', 'to':  'BillItem'}
]


DESCRIPTION_CONTRIBUTION_VALUATION = F'' \
    F'This calculation will, for the selected level and product,' \
    F' calculate how much the insurance need to' \
    F' the HF for the capitation financing'


CONTEXTS = ["BatchValuate", "BatchPayment", "IndividualPayment", "IndividualValuation"]


INTEGER_PARAMETERS = [
    "share_contribution", "weight_population", "weight_number_families", "weight_insured_population",
    "weight_number_insured_families", "weight_number_visits", "weight_adjusted_amount",
    "distr_1", "distr_2", "distr_3", "distr_4", "distr_5", "distr_6",
    "distr_7", "distr_8", "distr_9", "distr_10", "distr_11", "distr_12",
]


NONE_INTEGER_PARAMETERS = ['hf_level_1',
                           'hf_sublevel_1',
                           'hf_level_2',
                           'hf_sublevel_2',
                           'hf_level_3',
                           'hf_sublevel_3',
                           'hf_level_4',
                           'hf_sublevel_4']
