#include <stdio.h>

int main()
{
    FILE *file;

    int roll;
    char name[50];
    char status;

    file = fopen("../data/attendance.txt", "a");

    if(file == NULL)
    {
        printf("Error opening file!");
        return 1;
    }

    printf("Enter Roll Number: ");
    scanf("%d", &roll);

    printf("Enter Name: ");
    scanf("%s", name);

    printf("Enter Attendance (P/A): ");
    scanf(" %c", &status);

    fprintf(file, "%d %s %c\n", roll, name, status);

    fclose(file);

    printf("Attendance Saved Successfully!\n");

    return 0;
}
