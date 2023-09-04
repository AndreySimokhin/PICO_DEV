from config import Element, Config
import asyncio


el1 = Element(entry_id='1', title='Title1', data={'start': True, 'dev_mode': False})
el2 = Element(entry_id='2', title='Title2', data={'start': False, 'dev_mode': False})

conf = Config(path='config.json')

async def main():
    await conf.add(el1)
    await conf.add(el2)

    await conf.load_config()
    print(conf)
    print(conf['1'])
    print(conf['2'].entry_id)

if __name__ == '__main__':
    asyncio.run(main())
