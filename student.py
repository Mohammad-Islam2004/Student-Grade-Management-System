import json
import random
import string
from pathlib import Path

class Student:
    database = 'data.json'
    
    def __init__(self):
        self.path = Path(self.database)
        self.data = json.loads(self.path.read_text()) if self.path.exists() else []
        
    def _save(self):
        self.path.write_text(json.dumps(self.data, indent=4))
        
    def _id(self):
        # Generates a unique roll number matching your original logic (e.g., AB123)
        return ''.join(random.choices(string.ascii_uppercase, k=2) + random.choices(string.digits, k=3))
        
    def add_student(self, name, age, course):
        s = {
            "roll_no": self._id(),
            "name": name,
            "age": int(age),
            "course": course,
            "marks": {},
            "percentage": 0.0,
            "grade": "F"
        }
        self.data.append(s)
        self._save()
        return s
        
    def get(self, r):
        return next((x for x in self.data if x["roll_no"].strip().upper() == r.strip().upper()), None)
        
    def update(self, r, **kw):
        s = self.get(r)
        if not s:
            return False
        for k, v in kw.items():
            if v is not None:
                if k == "age":
                    s[k] = int(v)
                else:
                    s[k] = v
        self._save()
        return True
        
    def delete(self, r):
        s = self.get(r)
        if not s:
            return False
        self.data.remove(s)
        self._save()
        return True
        
    def add_marks(self, r, sub, m):
        s = self.get(r)
        if not s:
            return False
        s["marks"][sub] = int(m)
        self.calc(r)
        return True

    def delete_mark(self, r, sub):
        s = self.get(r)
        if not s or sub not in s["marks"]:
            return False
        del s["marks"][sub]
        self.calc(r)
        return True
        
    def calc(self, r):
        s = self.get(r)
        if not s:
            return
        vals = list(s["marks"].values())
        p = sum(vals) / len(vals) if vals else 0.0
        s["percentage"] = round(p, 2)
        s["grade"] = "A" if p >= 90 else "B" if p >= 80 else "C" if p >= 70 else "D" if p >= 60 else "F"
        self._save()
        return s
        
    def stats(self):
        if not self.data:
            return {}
        per = [x["percentage"] for x in self.data]
        passed = sum(1 for x in per if x >= 35)
        total = len(per)
        return {
            "Total Students": total,
            "Average": round(sum(per) / total, 2) if total else 0.0,
            "Highest": max(per) if total else 0.0,
            "Lowest": min(per) if total else 0.0,
            "Passed": passed,
            "Failed": total - passed,
            "Pass Rate": round((passed / total) * 100, 2) if total else 0.0
        }