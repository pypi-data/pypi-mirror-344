# animact

Anime-themed action and reaction image API wrapper for Python.

![PyPI](https://img.shields.io/pypi/v/animact)
![License](https://img.shields.io/github/license/monabborhossain/animact)

---

## ✨ Features

- Simple API to fetch anime reaction/action images
- Over 50+ categories: hug, pat, slap, wave, etc.
- Both synchronous and asynchronous support
- Minimal dependencies
- Simple and easy-to-use
- Multiple import patterns for flexibility

---

## 🚀 Installation

```bash
pip install animact
```

---

## 📖 Usage

### Synchronous Usage

There are three ways to use the synchronous API:

1. **Direct Function Import** (Simplest)
```python
from animact import hug, pat
url = hug()
pat_url = pat()
```

2. **Using Default Instance**
```python
from animact import animact
url = animact.hug()
pat_url = animact.pat()
```

3. **Creating Custom Instance**
```python
from animact import Animact
client = Animact()
url = client.hug()
pat_url = client.pat()
```

### Asynchronous Usage

There are two ways to use the asynchronous API:

1. **Using Default Async Instance** (Recommended)
```python
import asyncio
from animact import async_animact

async def main():
    url = await async_animact.hug()
    pat_url = await async_animact.pat()

asyncio.run(main())
```

2. **Creating Custom Async Instance**
```python
import asyncio
from animact import AsyncAnimact

async def main():
    client = AsyncAnimact()
    url = await client.hug()
    pat_url = await client.pat()

asyncio.run(main())
```

### Complete Example

```python
import asyncio
from animact import (
    # Sync imports
    hug, pat,  # Direct functions
    animact,   # Default sync instance
    Animact,   # Sync class
    # Async imports
    async_animact,  # Default async instance
    AsyncAnimact    # Async class
)

# Synchronous usage
print("Sync - Direct functions:")
print(hug())
print(pat())

print("\nSync - Default instance:")
print(animact.hug())
print(animact.pat())

# Asynchronous usage
async def main():
    print("\nAsync - Default instance:")
    print(await async_animact.hug())
    print(await async_animact.pat())
    
    print("\nAsync - Custom instance:")
    client = AsyncAnimact()
    print(await client.hug())
    print(await client.pat())

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📚 Available Actions

All these actions are available in both synchronous and asynchronous versions:

- lurk
- shoot
- sleep
- shrug
- stare
- wave
- poke
- smile
- peck
- wink
- blush
- smug
- tickle
- yeet
- think
- highfive
- feed
- bite
- bored
- nom
- yawn
- facepalm
- cuddle
- kick
- happy
- hug
- baka
- pat
- angry
- run
- nod
- nope
- kiss
- dance
- punch
- handshake
- slap
- cry
- pout
- handhold
- thumbsup
- laugh
- bully
- lick
- bonk
- glomp
- kill
- cringe
- spank

---

## 🌟 Star This Project

If you like this project, please consider [starring it on GitHub](https://github.com/monabborhossain/animact) — it really helps!

---

## 🧑‍💻 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## 📄 License

MIT License — see `LICENSE` file for details.

---

## ☕ Support Me

[![Buy Me a Coffee](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/monabborhossain)
