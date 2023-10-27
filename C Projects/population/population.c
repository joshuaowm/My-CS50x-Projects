#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    int s;
    // TODO: Prompt for start size
    do
    {
        s = get_int("Start size: ");
    }
    while (s < 9);

    // TODO: Prompt for end size
    int e;
    do
    {
        e = get_int("End size: ");
    }
    while (e < s);

    // TODO: Calculate number of years until we reach threshold
    int y = 0;
    while (s < e)
    {
        s = s + (s / 3) - (s / 4);
        y++;
    }

    // TODO: Print number of years
    printf("Years: %i\n", y);
}
