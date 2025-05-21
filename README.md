# Kitchensink modernizer: Java Code Annotation and Modernization Tool

This tool allows you to annotate and modernize legacy Java code using the Google Gemini API. It supports line-by-line inline comments, full code modernization (e.g., migrating to Spring Boot), and even provides recommendations for adapting traditional JPA code to MongoDB.

## 🚀 Features

- Supports Google Gemini GenAI API
- Works on individual files with `.java` extension (can be extended to other code types)
- Modes: `comment` (adds inline explanation) and `modernize` (suggests architectural updates)
- GUI with drag-and-drop support
- Command-line interface
- Can be imported and used directly as a Python module

---

## 🛠️ Setup Instructions

1. **Clone this repository**

```bash
git clone https://github.com/shijiahuang/kitchensink-modernizer.git
```

2. **Create and Activate a Conda Environment**

```bash
conda create -n kitchen-upgrade python=3.10
conda activate kitchen-upgrade
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install python-dotenv google-generativeai tkinterdnd2
```

4. **Create a `.env` File**

```bash
cp .env.example .env
```

Edit `.env` and replace with your Google Gemini API key:
```
GOOGLE_API_KEY=your_google_api_key_here
```

---

## 💻 How to Use

### 1. Run the GUI App

```bash
python UI.py
```

- **Input File Path**: Use the file browser or drag a `.java` file here.
- **Output File Path** (optional): If left blank, a new file will be created with `_comment` or `_modernize` suffix.
- Click **Comment** to add inline documentation.
- Click **Modernize** to generate a refactored version using modern Java practices.

### 2. Use the CLI

```bash
python analyze_code.py path/to/InputFile.java --mode comment
```

- Modes:
  - `comment`: Adds inline explanation.
  - `modernize`: Suggests and outputs updated version.

### 3. Use as a Python Function (For Developers)

If you are a developer and prefer not to use the GUI, you can import and run the core functionality in your own script:

```python
from analyze_code import analyze_code

analyze_code("path/to/InputFile.java", "path/to/OutputFile.java", mode="comment")
```

A sample script is included as `demo_script.py`. To test it, run:

```bash
python demo_script.py
```

This is useful for automation or integrating the tool into your own pipelines.
Make sure your `.env` file is present or set `GOOGLE_API_KEY` in your environment variables.

---

## 📂 Output

- A new file will be created (e.g., `InputFile_commented.java`)
- Contains the original code with AI-generated inline comments or a rewritten, modernized version.

---

## ✅ Tips

- Use small to medium sized files to stay within token limits.
- Modernization results are suggestions—manual review is recommended.

---

## 🔁 Example: Before and After Modernization

### Before:
```java
@ApplicationScoped
public class MemberRepository {
    @Inject
    private EntityManager em;

    public Member findById(Long id) {
        return em.find(Member.class, id);
    }

    public Member findByEmail(String email) {
        CriteriaBuilder cb = em.getCriteriaBuilder();
        CriteriaQuery<Member> criteria = cb.createQuery(Member.class);
        Root<Member> member = criteria.from(Member.class);
        criteria.select(member).where(cb.equal(member.get("email"), email));
        return em.createQuery(criteria).getSingleResult();
    }
}
```

### After:
```java
@Repository // Marks this class as a Spring Data Repository
@Transactional // Ensures methods are executed within a transaction
public class MemberRepository {

    @Autowired
    private EntityManager em;

    public Optional<Member> findById(Long id) {
        Member member = em.find(Member.class, id);
        return Optional.ofNullable(member); // Handle null safely
    }

    public Optional<Member> findByEmail(String email) {
        CriteriaBuilder cb = em.getCriteriaBuilder();
        CriteriaQuery<Member> criteria = cb.createQuery(Member.class);
        Root<Member> member = criteria.from(Member.class);
        criteria.select(member).where(cb.equal(member.get("email"), email));

        try {
            return Optional.of(em.createQuery(criteria).getSingleResult());
        } catch (NoResultException e) {
            return Optional.empty(); // Return empty Optional if no result
        }
    }
}
```

---

## 🖼️ GUI Preview

Here's a screenshot of the GUI application:
![screenshot](images/gui_demo.png)

---

## 🐳 Run with Docker

You can run this tool inside a Docker container without needing to set up a Python environment.
This is especially useful for users who are not familiar with setting up Python or Java environments.

### 1. Build the Docker image
```bash
docker build -t kitchen-upgrade .
```

### 2. Run the tool in CLI mode

You can choose one of two modes depending on your goal:

#### Option A – Add Inline Comments
```bash
docker run -it --rm \
  -v $(pwd):/app \  # Mounts this tool's folder (should contain analyze_code.py)
  -v /absolute/path/to/your/java/project:/project \  # Mounts your external Java project (in this case it is kitchensink) 
  # (copying mine here for more accessible demo)
  # -v /Users/shijia_huang/Desktop/kitchen_sink/jboss-eap-quickstarts/kitchensink:/project \ 
  -e GOOGLE_API_KEY=your_real_key \
  kitchen-upgrade /project/path/to/YourFile.java --mode comment
```
This will produce a new file like `YourFile_commented.java` with inline explanations.

#### Option B – Modernize the Code
```bash
docker run -it --rm \
  -v $(pwd):/app \
  -e GOOGLE_API_KEY=your_real_key \
  kitchen-upgrade /project/path/to/YourFile.java  --mode modernize
```
This will produce a modernized Java version like `YourFile_modernized.java`.

### 3. Optionally use a .env file
If you already have a `.env` file that contains your Gemini API key:
```bash
docker run --rm --env-file .env -v $(pwd):/app kitchen-upgrade path/to/InputFile.java --mode comment
```

### 🔐 About the API Key
By default, the Dockerfile includes a placeholder `ENV GOOGLE_API_KEY=your_key_here`, but **you should never hard-code your API key directly into the Dockerfile.**

Instead, pass your API key securely at runtime using:
- `-e GOOGLE_API_KEY=your_real_key` or
- `--env-file .env`

---

## Extract Code Structure

For developers or reviewers who want to understand the class structure of a Java file, this project includes a structure analysis utility.

### How to use

First, install the required dependency:

```bash
pip install javalang
```

Then run:

```bash
python code_structure.py path/to/YourFile.java -o output/structure_summary.md
```

This will generate a Markdown file listing all classes, fields, and method signatures.

### Example output

```markdown
## Class: MemberRepository

### Fields:
- EntityManager em

### Methods:
- findById(Long id)
- findByEmail(String email)
- findAllOrderedByName()
```

---
## 🧠 AI-Powered MongoDB Recommendation (Built-in)

When you use the `modernize` mode, the Gemini API is instructed not only to rewrite legacy Java into Spring Boot-style code, but also to intelligently detect whether MongoDB would be a more suitable backend than traditional JPA.

If the original code includes patterns like `@Entity`, `EntityManager`, or `@PersistenceContext`, the AI will automatically:

- Flag that a NoSQL migration could be considered
- Suggest replacing JPA annotations with `@Document`
- Propose `MongoRepository`-based interfaces instead of manual persistence logic

This recommendation logic is embedded directly in the prompt used by the tool. No manual editing is required—you will see MongoDB suggestions directly in the generated output when applicable.

This feature complements the optional MongoDB migration guide provided below.

## 💡 Optional: Recommendations for MongoDB Migration

The legacy kitchensink application relies on relational database access using JPA and `EntityManager`. To modernize and prepare the application for NoSQL environments such as MongoDB, the following recommendations can be considered:

### 🧠 Why consider MongoDB?

- 📄 Flexible document schemas — easier to evolve data models over time
- ☁️ Better suited for microservices and cloud-native architectures
- 🛠️ Reduced setup — no need for strict table relationships or SQL schemas

### 🔁 Suggested Changes

1. **Entity Conversion**  
   Replace JPA `@Entity` with MongoDB's `@Document`, and use `String` IDs (e.g., UUID or ObjectId).

   **Before (JPA):**
   ```java
   @Entity
   public class Member {
       @Id
       private Long id;
       private String email;
   }
   ```

   **After (MongoDB):**
   ```java
   @Document(collection = "members")
   public class Member {
       @Id
       private String id;
       private String email;
   }
   ```

2. **Repository Refactor**  
   Replace `EntityManager` with `MongoRepository` to simplify data access.

   **Before:**
   ```java
   @PersistenceContext
   private EntityManager em;
   em.find(Member.class, id);
   ```

   **After:**
   ```java
   public interface MemberRepository extends MongoRepository<Member, String> {
       Optional<Member> findByEmail(String email);
   }
   ```

3. **MongoDB Configuration**  
   In your `application.properties`:

   ```
   spring.data.mongodb.uri=mongodb://localhost:27017
   spring.data.mongodb.database=kitchensink
   ```

### ✅ Final Note

These changes would align best with a migration to Spring Boot and Spring Data MongoDB.  
The modernization tool could be extended to **identify JPA usage** and **recommend NoSQL-ready alternatives**.

---

## 📧 Support

For bugs or feature requests, please contact [sjx2413@gmail.com] or open an issue.
