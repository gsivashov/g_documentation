with open('spendings.csv') as start_file:
    total_cost = 0

    for line in start_file:
        line = line.strip()
        name, price = line.split('|')
        total_cost += float(price)

    print(total_cost)
