from ro_py import Client
import asyncio, requests, time
from os import environ
cookie = environ['cookie']
client = Client(cookie)
group_id = 9722707

def ownsShirt(transactions, user_id):
    for purchase in transactions['data']:
        if purchase['agent']['id'] == user_id:
            if purchase['details']['name'] == "ITV Support Donation":
                return True
    return False
        
async def main():
    
    group = await client.get_group(group_id)

    while True:
        print('checking...')
        transactions = await group.get_transactions()
        pages = await group.get_members()
        members = []
        members += pages.data.data
        cursor = pages.data.next_page_cursor
        while cursor != None:
            pages.get_page(cursor)
            members += pages.data.data
            cursor = pages.data.next_page_cursor

        
        for member in members:
            
            rank = member['role']['rank']
            user_id = member['user']['userId']
            if rank == 1:
                if ownsShirt(transactions, user_id):
                    print('Giving Donor role to ' + str(user_id))

                    member = await group.get_member_by_id(user_id)
                    success = await member.setrole(250)
        time.sleep(10)
            


asyncio.get_event_loop().run_until_complete(main())
