# 📦 Jsonix

**Jsonix** is a lightweight and easy-to-use JSON manager for Python. It allows you to read, write, modify, and delete data in a JSON file without losing its structure. With path-based access, you can interact with any `data.json` file in a straightforward and intuitive way.

---

## 🚀 Features

- ✅ **Add** data at any nested path (`add`)
- ✅ **Remove** data from a specified path (`remove`)
- ✅ **Change** existing data (`change`)
- ✅ **Get** data from any path (`get`)
- ✅ **Show** the entire JSON structure (`show`)
- ✅ **Clear** the entire JSON data (`clear`)
- ✅ **Auto-create** missing nested structures

---

## 📥 Installation

To install `Jsonix`, simply use `pip`:

```
pip install jsonix
```
Once installed, you can start using Jsonix to manage your JSON data easily:

Example:
```
from jsonix import jsonix
```
# Initialize with the path to your JSON file
```
json = jsonix.register("data.json")
```
# Add data to a nested path
```
json.add("hello,uz", "salom")
json.add("hello,ru", "привет")
```

# Get data from a path
```
print(json.get("hello,uz"))  # Output: salom
```

# Change data at a specific path
```
json.change("hello,ru", "Здравствуйте")
```
# Show the entire JSON data
```
print(json.show())
```

# Remove data from a specific path
```
json.remove("hello,ru")
```

# Clear the entire JSON file
```
json.clear()
```
Example Output:
```
{
  "hello": {
    "uz": "salom"
  }
}
```

**⚙️ Configuration and Customization**
The Jsonix library works by loading and saving the JSON file on every operation. It automatically handles missing paths and creates them when necessary. You can use it for various configurations and JSON structures.

**👨‍💻 Contributing**
Feel free to fork this repository, create a pull request, and submit any improvements or bug fixes. Contributions are always welcome!

**📄 License**
This project is licensed under the MIT License - see the LICENSE file for details.

## 📌 Links

- [YouTube](https://www.youtube.com/@axmadjonqaxxorovc)
- [Telegram](https://t.me/axmadjonqaxxorovc)
- [Taplink](https://taplink.cc/itsqaxxorov)