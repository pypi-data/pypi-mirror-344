# Explain-Log 🔥
> Understand your DevOps and Data Engineering logs instantly — powered by OpenAI.

---

## 🚀 What is Explain-Log?

**Explain-Log** is a colorful, intelligent command-line tool that reads any log file,  
explains the root cause of errors, and suggests fixes — powered by OpenAI's GPT models.

✅ Supports piped input from Kubernetes, Airflow, Spark, Jenkins, Terraform logs and more.  
✅ Provides clear warnings before sending logs externally.  
✅ Bright, beautiful CLI interface built with `rich`.

---

## 📦 Installation

**Option 1: From PyPI**

```bash
pip install explain-log
```

**Option 2: Using Docker**

```bash
docker pull yourdockerhubusername/explain-log
```

---

## 🛠 Usage

**Explain a log file:**

```bash
explain-log my-error.log
```

**Explain logs piped from another command:**

```bash
k logs my-pod-name -n my-namespace | explain-log --force
```

⚠️ When using piped input, you must add `--force` to skip manual confirmation.

---

## ⚙️ Options

| Option | Description |
|:---|:---|
| `--no-mask` | Disable auto-masking of sensitive data (emails, IPs, URLs) |
| `--force` | Skip security confirmation (required when piping logs) |

---

## 🎨 CLI Features

- Beautiful bright colored output
- Safety-first design (asks for confirmation before sending logs to OpenAI)
- Professional banners, warnings, and success messages
- Markdown-formatted explanations
- Works with stdin piping (`|`) or from log files

---

## 🛡 Security Notice

Explain-Log by default warns you and asks for your consent before sending any logs to OpenAI servers.  
You control when and what is sent.

---

## 🐳 Docker Usage

Run without installing Python:

```bash
docker run --rm yourdockerhubusername/explain-log --help
```

You can also pipe logs:

```bash
k logs mypod | docker run --rm -i yourdockerhubusername/explain-log --force
```

(Use `-i` to pass piped input into Docker.)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## ✨ Author

Made with ❤️ by [Your Name]  
GitHub: [github.com/yourgithub](https://github.com/yourgithub)

