import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.List;

/**
 * Student Management System - Java Swing GUI Application
 * 
 * Demonstrates OOP concepts: Encapsulation, Inheritance, Polymorphism,
 * Exception Handling, and GUI design with event-driven programming.
 * 
 * Course: Object Oriented Programming Lab (ICT 4252)
 * Student: Rayhanul Islam
 */

// ========== Encapsulation: Student Class ==========
class Student {
    private String id;
    private String name;
    private String email;
    private double gpa;

    public Student(String id, String name, String email, double gpa) {
        this.id = id;
        this.name = name;
        this.email = email;
        setGpa(gpa);
    }

    public String getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    public double getGpa() { return gpa; }

    public void setName(String name) { this.name = name; }
    public void setEmail(String email) { this.email = email; }

    public void setGpa(double gpa) {
        if (gpa < 0.0 || gpa > 4.0) {
            throw new IllegalArgumentException("GPA must be between 0.0 and 4.0");
        }
        this.gpa = gpa;
    }

    public String getGrade() {
        if (gpa >= 3.7) return "A";
        if (gpa >= 3.3) return "A-";
        if (gpa >= 3.0) return "B+";
        if (gpa >= 2.7) return "B";
        if (gpa >= 2.3) return "B-";
        if (gpa >= 2.0) return "C+";
        if (gpa >= 1.0) return "C";
        return "F";
    }

    @Override
    public String toString() {
        return String.format("Student{id='%s', name='%s', gpa=%.2f, grade='%s'}",
                id, name, gpa, getGrade());
    }
}

// ========== Inheritance: GraduateStudent extends Student ==========
class GraduateStudent extends Student {
    private String researchArea;

    public GraduateStudent(String id, String name, String email, double gpa, String researchArea) {
        super(id, name, email, gpa);
        this.researchArea = researchArea;
    }

    public String getResearchArea() { return researchArea; }
    public void setResearchArea(String researchArea) { this.researchArea = researchArea; }

    @Override
    public String toString() {
        return String.format("GradStudent{id='%s', name='%s', gpa=%.2f, research='%s'}",
                getId(), getName(), getGpa(), researchArea);
    }
}

// ========== Custom Exception ==========
class StudentNotFoundException extends Exception {
    public StudentNotFoundException(String message) {
        super(message);
    }
}

// ========== Student Manager (Model) ==========
class StudentManager {
    private List<Student> students;

    public StudentManager() {
        students = new ArrayList<>();
    }

    public void addStudent(Student s) throws IllegalArgumentException {
        for (Student existing : students) {
            if (existing.getId().equals(s.getId())) {
                throw new IllegalArgumentException("Student with ID " + s.getId() + " already exists.");
            }
        }
        students.add(s);
    }

    public void removeStudent(String id) throws StudentNotFoundException {
        Student student = findStudent(id);
        students.remove(student);
    }

    public Student findStudent(String id) throws StudentNotFoundException {
        for (Student s : students) {
            if (s.getId().equals(id)) {
                return s;
            }
        }
        throw new StudentNotFoundException("Student with ID " + id + " not found.");
    }

    public void updateStudent(String id, String name, String email, double gpa) throws StudentNotFoundException {
        Student s = findStudent(id);
        s.setName(name);
        s.setEmail(email);
        s.setGpa(gpa);
    }

    public List<Student> getAllStudents() {
        return new ArrayList<>(students);
    }

    public double getAverageGpa() {
        if (students.isEmpty()) return 0.0;
        double sum = 0;
        for (Student s : students) {
            sum += s.getGpa();
        }
        return sum / students.size();
    }
}

// ========== Polymorphism: GradeCalculator Interface ==========
interface GradeCalculator {
    String calculate(double gpa);
}

class StandardGradeCalculator implements GradeCalculator {
    @Override
    public String calculate(double gpa) {
        if (gpa >= 3.7) return "A";
        if (gpa >= 3.0) return "B";
        if (gpa >= 2.0) return "C";
        if (gpa >= 1.0) return "D";
        return "F";
    }
}

class DetailedGradeCalculator implements GradeCalculator {
    @Override
    public String calculate(double gpa) {
        if (gpa >= 3.7) return "A (Excellent)";
        if (gpa >= 3.3) return "A- (Very Good)";
        if (gpa >= 3.0) return "B+ (Good)";
        if (gpa >= 2.7) return "B (Above Average)";
        if (gpa >= 2.3) return "B- (Average)";
        if (gpa >= 2.0) return "C+ (Below Average)";
        if (gpa >= 1.0) return "C (Poor)";
        return "F (Failing)";
    }
}

// ========== Main GUI Application ==========
public class StudentManagementApp extends JFrame {
    private StudentManager manager;
    private JTable table;
    private DefaultTableModel tableModel;
    private JTextField idField, nameField, emailField, gpaField;
    private JLabel statusLabel;
    private GradeCalculator gradeCalc;

    public StudentManagementApp() {
        manager = new StudentManager();
        gradeCalc = new DetailedGradeCalculator();
        initComponents();
        loadSampleData();
        refreshTable();
    }

    private void initComponents() {
        setTitle("Student Management System - OOP Demo");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(800, 600);
        setLocationRelativeTo(null);

        // Menu Bar
        JMenuBar menuBar = new JMenuBar();
        JMenu fileMenu = new JMenu("File");
        JMenuItem exitItem = new JMenuItem("Exit");
        exitItem.addActionListener(e -> System.exit(0));
        fileMenu.add(exitItem);
        menuBar.add(fileMenu);

        JMenu helpMenu = new JMenu("Help");
        JMenuItem aboutItem = new JMenuItem("About");
        aboutItem.addActionListener(e -> JOptionPane.showMessageDialog(this,
                "Student Management System\nOOP Demo Application\n\n"
                + "Demonstrates: Encapsulation, Inheritance,\n"
                + "Polymorphism, Exception Handling, GUI Design",
                "About", JOptionPane.INFORMATION_MESSAGE));
        helpMenu.add(aboutItem);
        menuBar.add(helpMenu);
        setJMenuBar(menuBar);

        // Input Panel
        JPanel inputPanel = new JPanel(new GridBagLayout());
        inputPanel.setBorder(BorderFactory.createTitledBorder("Student Information"));
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(4, 4, 4, 4);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        gbc.gridx = 0; gbc.gridy = 0;
        inputPanel.add(new JLabel("ID:"), gbc);
        gbc.gridx = 1;
        idField = new JTextField(15);
        inputPanel.add(idField, gbc);

        gbc.gridx = 0; gbc.gridy = 1;
        inputPanel.add(new JLabel("Name:"), gbc);
        gbc.gridx = 1;
        nameField = new JTextField(15);
        inputPanel.add(nameField, gbc);

        gbc.gridx = 2; gbc.gridy = 0;
        inputPanel.add(new JLabel("Email:"), gbc);
        gbc.gridx = 3;
        emailField = new JTextField(15);
        inputPanel.add(emailField, gbc);

        gbc.gridx = 2; gbc.gridy = 1;
        inputPanel.add(new JLabel("GPA:"), gbc);
        gbc.gridx = 3;
        gpaField = new JTextField(15);
        inputPanel.add(gpaField, gbc);

        // Buttons
        JPanel buttonPanel = new JPanel(new FlowLayout());
        JButton addBtn = new JButton("Add");
        JButton updateBtn = new JButton("Update");
        JButton deleteBtn = new JButton("Delete");
        JButton clearBtn = new JButton("Clear");
        JButton findBtn = new JButton("Find");

        addBtn.addActionListener(new AddButtonListener());
        updateBtn.addActionListener(new UpdateButtonListener());
        deleteBtn.addActionListener(new DeleteButtonListener());
        clearBtn.addActionListener(e -> clearFields());
        findBtn.addActionListener(new FindButtonListener());

        buttonPanel.add(addBtn);
        buttonPanel.add(updateBtn);
        buttonPanel.add(deleteBtn);
        buttonPanel.add(findBtn);
        buttonPanel.add(clearBtn);

        gbc.gridx = 0; gbc.gridy = 2; gbc.gridwidth = 4;
        inputPanel.add(buttonPanel, gbc);

        // Table
        String[] columns = {"ID", "Name", "Email", "GPA", "Grade", "Type"};
        tableModel = new DefaultTableModel(columns, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
        table = new JTable(tableModel);
        table.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        table.getSelectionModel().addListSelectionListener(e -> {
            if (!e.getValueIsAdjusting()) {
                selectRow();
            }
        });

        JScrollPane scrollPane = new JScrollPane(table);

        // Status Bar
        statusLabel = new JLabel("Ready | Students: 0 | Average GPA: 0.00");
        statusLabel.setBorder(BorderFactory.createEtchedBorder());

        // Layout
        setLayout(new BorderLayout());
        add(inputPanel, BorderLayout.NORTH);
        add(scrollPane, BorderLayout.CENTER);
        add(statusLabel, BorderLayout.SOUTH);
    }

    private void loadSampleData() {
        try {
            manager.addStudent(new Student("STU001", "Rahul Ahmed", "rahul@uftb.edu", 3.5));
            manager.addStudent(new GraduateStudent("STU002", "Fatema Khatun", "fatema@uftb.edu", 3.8, "Machine Learning"));
            manager.addStudent(new Student("STU003", "Kamal Hossain", "kamal@uftb.edu", 2.8));
            manager.addStudent(new GraduateStudent("STU004", "Nusrat Jahan", "nusrat@uftb.edu", 3.2, "Data Science"));
            manager.addStudent(new Student("STU005", "Ariful Islam", "arif@uftb.edu", 2.5));
        } catch (IllegalArgumentException e) {
            // Duplicate ID, skip
        }
    }

    private void refreshTable() {
        tableModel.setRowCount(0);
        for (Student s : manager.getAllStudents()) {
            String type = s instanceof GraduateStudent ? "Graduate" : "Undergraduate";
            tableModel.addRow(new Object[]{
                    s.getId(), s.getName(), s.getEmail(),
                    String.format("%.2f", s.getGpa()),
                    gradeCalc.calculate(s.getGpa()),
                    type
            });
        }
        updateStatusBar();
    }

    private void updateStatusBar() {
        statusLabel.setText(String.format("Ready | Students: %d | Average GPA: %.2f",
                manager.getAllStudents().size(), manager.getAverageGpa()));
    }

    private void selectRow() {
        int row = table.getSelectedRow();
        if (row >= 0) {
            idField.setText((String) tableModel.getValueAt(row, 0));
            nameField.setText((String) tableModel.getValueAt(row, 1));
            emailField.setText((String) tableModel.getValueAt(row, 2));
            gpaField.setText((String) tableModel.getValueAt(row, 3));
            idField.setEditable(false);
        }
    }

    private void clearFields() {
        idField.setText("");
        nameField.setText("");
        emailField.setText("");
        gpaField.setText("");
        idField.setEditable(true);
        table.clearSelection();
    }

    // ========== Event Listeners (Event-Driven Programming) ==========
    private class AddButtonListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            try {
                String id = idField.getText().trim();
                String name = nameField.getText().trim();
                String email = emailField.getText().trim();
                double gpa = Double.parseDouble(gpaField.getText().trim());

                if (id.isEmpty() || name.isEmpty() || email.isEmpty()) {
                    JOptionPane.showMessageDialog(StudentManagementApp.this,
                            "All fields are required.", "Validation Error", JOptionPane.WARNING_MESSAGE);
                    return;
                }

                manager.addStudent(new Student(id, name, email, gpa));
                refreshTable();
                clearFields();
                JOptionPane.showMessageDialog(StudentManagementApp.this,
                        "Student added successfully!", "Success", JOptionPane.INFORMATION_MESSAGE);
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(StudentManagementApp.this,
                        "GPA must be a valid number.", "Input Error", JOptionPane.ERROR_MESSAGE);
            } catch (IllegalArgumentException ex) {
                JOptionPane.showMessageDialog(StudentManagementApp.this,
                        ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private class UpdateButtonListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            try {
                String id = idField.getText().trim();
                String name = nameField.getText().trim();
                String email = emailField.getText().trim();
                double gpa = Double.parseDouble(gpaField.getText().trim());

                manager.updateStudent(id, name, email, gpa);
                refreshTable();
                clearFields();
                JOptionPane.showMessageDialog(StudentManagementApp.this,
                        "Student updated successfully!", "Success", JOptionPane.INFORMATION_MESSAGE);
            } catch (StudentNotFoundException ex) {
                JOptionPane.showMessageDialog(StudentManagementApp.this,
                        ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(StudentManagementApp.this,
                        "GPA must be a valid number.", "Input Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private class DeleteButtonListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            try {
                String id = idField.getText().trim();
                int confirm = JOptionPane.showConfirmDialog(StudentManagementApp.this,
                        "Are you sure you want to delete student " + id + "?",
                        "Confirm Delete", JOptionPane.YES_NO_OPTION);

                if (confirm == JOptionPane.YES_OPTION) {
                    manager.removeStudent(id);
                    refreshTable();
                    clearFields();
                    JOptionPane.showMessageDialog(StudentManagementApp.this,
                            "Student deleted successfully!", "Success", JOptionPane.INFORMATION_MESSAGE);
                }
            } catch (StudentNotFoundException ex) {
                JOptionPane.showMessageDialog(StudentManagementApp.this,
                        ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private class FindButtonListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            try {
                String id = idField.getText().trim();
                Student s = manager.findStudent(id);
                nameField.setText(s.getName());
                emailField.setText(s.getEmail());
                gpaField.setText(String.format("%.2f", s.getGpa()));
                idField.setEditable(false);

                for (int i = 0; i < tableModel.getRowCount(); i++) {
                    if (tableModel.getValueAt(i, 0).equals(id)) {
                        table.setRowSelectionInterval(i, i);
                        break;
                    }
                }
            } catch (StudentNotFoundException ex) {
                JOptionPane.showMessageDialog(StudentManagementApp.this,
                        ex.getMessage(), "Not Found", JOptionPane.WARNING_MESSAGE);
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
            } catch (Exception ignored) {}
            new StudentManagementApp().setVisible(true);
        });
    }
}
