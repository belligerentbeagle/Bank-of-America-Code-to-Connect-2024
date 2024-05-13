# Bank of America Code to Connect 2024
 Coding competition held on the 13th of May 2024! Let's see where ambition takes us!

 Welcome to team ACE! Below are the instructions on how to use our program!

# How to use
Command format: `python3 matcher.py path_to_input_orders.csv path_to_input_clients.csv path_to_input_instruments.csv`

and the output reports will be generated in the directory of matcher.py!

Example:
```
/opt/homebrew/bin/python3 /Users/ethanyuxin/Documents/World/Bank-of-America-Code-to-Connect-2024/matcher.py ./DataSets/example-set/input_orders.csv ./DataSets/example-set/input_clients.csv ./DataSets/example-set/input_instruments.csv
```

# Architecure Diagram




# Testing

# Policy testing
Client F is eligible for trading USD but tries to make order for instrument using SGD.

Lot size test check:
Order E5 attempts SIA stock order with 2020, not a multiple of 100.

# Edge case to consider
If Client A makes a buy order of 100, but it is never/not yet fulfilled, then he makes a sell order of 100, it has to be rejected