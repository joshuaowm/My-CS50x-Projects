#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    //Ask for credit number
    const long number = get_long("Number: ");
    
    //Luhn algorithm
    long l1, d1;
    long i = 0;
    for (d1 = 10; d1 < number; d1 *= 100)
    {
        l1 = number / d1 % 10 * 2;
        if (l1 > 9)
        {
            int l3 = l1 / 10;
            int l4 = l1 % 10;
            i = i + l3 + l4;
        }
        else
        {
            i = i + l1;
        }
    }
    long l2, d2;
    long j = 0;
    for (d2 = 1; d2 < number; d2 *= 100)
    {
        l2 = number / d2 % 10;
        j = j + l2;
    }
    int x = (i + j);

    //Check length and digits
    long k = number;
    int count = 0;
    do
    {
        k = k / 10;
        count++;
    }
    while (k != 0);

    //Credit card type
    long mc = 1;
    long sa = 1;
    for (long ae = 0; ae < count - 2; ae++)
    {
        mc = mc * 10;
    }
    for (long vi = 0; vi < count - 1; vi++)
    {
        sa = sa * 10;
    }
    int aemc = number / mc;
    int visa = number / sa;

    //Print credit card type
    if (x % 10 == 0)
    {
        if ((count == 15) && (aemc == 34 || aemc == 37))
        {
            printf("AMEX\n");
        }
        else if ((count == 16) && (aemc > 50 && aemc < 56))
        {
            printf("MASTERCARD\n");
        }
        else if ((count == 13 || count == 16) && (visa == 4))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}