#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get height input
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    //Calculate the input
    for (int row = 0; row < height; row++)
    {
        for (int space = row + 1; space < height; space++) //Count the spaces needed
        {
            printf(" ");
        }
        for (int hash = height - row; hash < height + 1; hash++) //Count the hashes needed (left)
        {
            printf("#");
        }
        printf("  "); //Print the gap
        for (int hash = height - row; hash < height + 1; hash++) //Count the hashes needed (right)
        {
            printf("#");
        }
        printf("\n");
    }
}