import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for Student Management System OOP classes.
 * 
 * Tests demonstrate exception handling, encapsulation, and inheritance.
 */
public class StudentTest {

    private Student student;
    private GraduateStudent gradStudent;

    @BeforeEach
    void setUp() {
        student = new Student("STU001", "Test Student", "test@uftb.edu", 3.5);
        gradStudent = new GraduateStudent("STU002", "Grad Student", "grad@uftb.edu", 3.8, "AI");
    }

    @Test
    void testStudentCreation() {
        assertEquals("STU001", student.getId());
        assertEquals("Test Student", student.getName());
        assertEquals("test@uftb.edu", student.getEmail());
        assertEquals(3.5, student.getGpa(), 0.001);
    }

    @Test
    void testStudentGrade() {
        assertEquals("A", student.getGrade());

        Student bStudent = new Student("S2", "B Student", "b@test.com", 2.8);
        assertEquals("B", bStudent.getGrade());

        Student fStudent = new Student("S3", "F Student", "f@test.com", 0.5);
        assertEquals("F", fStudent.getGrade());
    }

    @Test
    void testStudentSetters() {
        student.setName("Updated Name");
        assertEquals("Updated Name", student.getName());

        student.setEmail("updated@test.com");
        assertEquals("updated@test.com", student.getEmail());

        student.setGpa(3.9);
        assertEquals(3.9, student.getGpa(), 0.001);
    }

    @Test
    void testInvalidGpaThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> {
            student.setGpa(5.0);
        });
        assertThrows(IllegalArgumentException.class, () -> {
            student.setGpa(-1.0);
        });
    }

    @Test
    void testGraduateStudentInheritance() {
        assertTrue(gradStudent instanceof Student);
        assertEquals("AI", gradStudent.getResearchArea());
        assertEquals("STU002", gradStudent.getId());
        assertEquals(3.8, gradStudent.getGpa(), 0.001);
    }

    @Test
    void testGraduateStudentResearchArea() {
        gradStudent.setResearchArea("Data Science");
        assertEquals("Data Science", gradStudent.getResearchArea());
    }

    @Test
    void testStudentManager() throws Exception {
        StudentManager manager = new StudentManager();
        manager.addStudent(new Student("S1", "One", "one@test.com", 3.0));
        manager.addStudent(new Student("S2", "Two", "two@test.com", 3.5));

        assertEquals(2, manager.getAllStudents().size());
        assertEquals(3.25, manager.getAverageGpa(), 0.001);
    }

    @Test
    void testDuplicateIdThrowsException() {
        StudentManager manager = new StudentManager();
        manager.addStudent(new Student("S1", "One", "one@test.com", 3.0));

        assertThrows(IllegalArgumentException.class, () -> {
            manager.addStudent(new Student("S1", "Duplicate", "dup@test.com", 2.5));
        });
    }

    @Test
    void testFindNonexistentStudentThrowsException() {
        StudentManager manager = new StudentManager();
        assertThrows(StudentNotFoundException.class, () -> {
            manager.findStudent("NONEXISTENT");
        });
    }

    @Test
    void testGradeCalculatorPolymorphism() {
        GradeCalculator standard = new StandardGradeCalculator();
        GradeCalculator detailed = new DetailedGradeCalculator();

        String sResult = standard.calculate(3.5);
        String dResult = detailed.calculate(3.5);

        assertEquals("A", sResult);
        assertTrue(dResult.contains("Very Good"));
    }
}
