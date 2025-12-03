data = "17330-35281,9967849351-9967954114,880610-895941,942-1466,117855-209809,9427633930-9427769294,1-14,311209-533855,53851-100089,104-215,33317911-33385573,42384572-42481566,43-81,87864705-87898981,258952-303177,451399530-451565394,6464564339-6464748782,1493-2439,9941196-10054232,2994-8275,6275169-6423883,20-41,384-896,2525238272-2525279908,8884-16221,968909030-969019005,686256-831649,942986-986697,1437387916-1437426347,8897636-9031809,16048379-16225280"

range_list = data.strip().split(',')
total_sum = 0

for r in range_list:
    start, end = map(int, r.split('-'))
    
    for num in range(start, end + 1):
        s = str(num)
        length = len(s)
        
        # Loop through possible pattern lengths
        # A pattern must repeat at least twice, so max pattern length is half the string
        for p_len in range(1, (length // 2) + 1):
            
            # 1. Logic Check: The pattern length must divide evenly into the total length
            if length % p_len == 0:
                
                # 2. Extract the potential pattern
                pattern = s[:p_len]
                
                # 3. Calculate how many times it needs to repeat
                multiplier = length // p_len
                
                # 4. Check if the pattern repeated matches the original string
                if pattern * multiplier == s:
                    total_sum += num
                    break # Important: Break so we don't count the same number twice!

print(total_sum)