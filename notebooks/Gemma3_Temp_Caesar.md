# Gemma3_Temp_Caesar.nb

## 1. Create Encoded Phrase

```mathematica
ResourceFunction["CaesarCipher"]["I think therefore I am", 5]
(* create an encoded phrase using an input phrase *)
```

**Output:**
```
"N ymnsp ymjwjktwj N fr"
```

## 2. Single Model Test (Gemma 3 12b)

```mathematica
Table[
    LLMSynthesize["you are an expert code-breaker, here is a coded message:'N ymnsp ymjwjktwj N fr', decipher it and respond with the deciphered message only", 
        LLMEvaluator -> LLMConfiguration[Association[
            "Model" -> {"Ollama", "gemma3:12b"}, 
            "Temperature" -> 1
        ]]
    ], 
    5
]
(* using the encoded phrase, prompt a single ollama local model at a fixed temperature to decode the message here gemma3:12b was used *)
```

## 3. Main Experiment (All Sizes)

**Description:**
Adapting the previous code, four local gemma3 models of varying parameter sizes are prompted to decipher the encoded phrase over a range of temperatures from 0 to 2, 0.1 incriments, each temperature repeated 25 times, the data is collected into an array which is exported to excel spreadsheet.

```mathematica
temps = Range[0, 2, 0.2];

G1B = Table[
    Table[
        LLMSynthesize["here is a coded message:'N ymnsp ymjwjktwj N fr', decipher it and respond with the deciphered message only", 
            LLMEvaluator -> LLMConfiguration[Association[
                "Model" -> {"Ollama", "gemma3:1b"}, 
                "Temperature" -> i
            ]]
        ],
        25
    ],
    {i, temps}
];
G1BT = Transpose[G1B];

G4B = Table[
    Table[
        LLMSynthesize["here is a coded message:'N ymnsp ymjwjktwj N fr', decipher it and respond with the deciphered message only", 
            LLMEvaluator -> LLMConfiguration[Association[
                "Model" -> {"Ollama", "gemma3:4b"}, 
                "Temperature" -> i
            ]]
        ],
        25
    ],
    {i, temps}
];
G4BT = Transpose[G4B];

G12B = Table[
    Table[
        LLMSynthesize["here is a coded message:'N ymnsp ymjwjktwj N fr', decipher it and respond with the deciphered message only", 
            LLMEvaluator -> LLMConfiguration[Association[
                "Model" -> {"Ollama", "gemma3:12b"}, 
                "Temperature" -> i
            ]]
        ],
        25
    ],
    {i, temps}
];
G12BT = Transpose[G12B];

G27B = Table[
    Table[
        LLMSynthesize["here is a coded message:'N ymnsp ymjwjktwj N fr', decipher it and respond with the deciphered message only", 
            LLMEvaluator -> LLMConfiguration[Association[
                "Model" -> {"Ollama", "gemma3:27b"}, 
                "Temperature" -> i
            ]]
        ],
        25
    ],
    {i, temps}
];
G27BT = Transpose[G27B];

Export["OL4file.xlsx", 
    {
        "G1B" -> G1BT, 
        "G4B" -> G4BT, 
        "G12B" -> G12BT, 
        "G27B" -> G27BT
    }, 
    "XLSX"
]
```
