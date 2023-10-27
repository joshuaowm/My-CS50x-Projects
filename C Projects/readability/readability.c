#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");

    double lett = count_letters(text);
    double word = count_words(text);
    double sent = count_sentences(text);

    //Coleman-Liau index
    double L = lett / word * 100;
    double S = sent / word * 100;
    double index = 0.0588 * L - 0.296 * S - 15.8;
    int rounded = round(index);

    //Print the grade level
    if (rounded < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (rounded >= 1 && rounded <= 15)
    {
        printf("Grade %i\n", rounded);
    }
    else
    {
        printf("Grade 16+\n");
    }
}

//Count letters
int count_letters(string text)
{
    int lett = 0;
    for (int i = 0, l = strlen(text); i < l; i++)
    {
        if (isalpha(text[i]))
        {
            lett += 1;
        }
        else
        {
            lett += 0;
        }
    }
    return lett;
}

//Count words
int count_words(string text)
{
    int word = 0;
    for (int i = 0, l = strlen(text); i < l; i++)
    {
        if (isspace(text[i]))
        {
            word += 1;
        }
        else
        {
            word += 0;
        }
    }
    word += 1;
    return word;
}

//Check sentences
int count_sentences(string text)
{
    int sent = 0;
    for (int i = 0, l = strlen(text); i < l; i++)
    {
        if (text[i] == 46 || text[i] == 33 || text[i] == 63)
        {
            sent += 1;
        }
        else
        {
            sent += 0;
        }
    }
    return sent;
}