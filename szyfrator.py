# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 23:24:06 2022

@author: Daniel Strzelecki


"""

class Szyfrator():
    '''
    This class provides a generator of polynomial encryption of ASCII
    passwords. You can take your favorite easy password and transform it
    into a harder one that satisfies the frequent condition
    (small letter, capital letter, digit, special character).
    The transformation is done in the following steps
    1. ''change_string_to_int''
        each character is changed to its ASCII code
        the string of all ASCII codes is produced 
        the string is divided into a list of ''seed''-digit numbers 
    2. ''poly_action_on_list'' 
        the value of polynomial is computed on each number from the list
    3. ''change_int_to_string''
        each number from list is transformed into ASCII code by modulo division
        the type of character is established on the first four places
    '''
    def __init__(self,seq,mode='const',seed=4):
        '''
        Parameters
        ----------
        seq : list of integers or integer number as a string
            The sequence of the coefficients to create polynomial coding 
            function
        mode : str, optional
            You can choose the mode. 'const' means the constant cipher,
            so to get different passwords you have to provide different 
            generators.
            The 'var' mode (not active so far) provides the different 
            encryption for different web sites and you can allways use your 
            favorite generator.
            The default is 'const'.
        seed : int, optional
            One can set the length of a single number the polynomial encryption 
            will be applied for. The longest seed you take the shortest 
            password you get.
            The default is 4.

        Raises
        ------
        ValueError
            Wrong values of element of string gives as seq.
        TypeError
            Wrong type of data given as seq.

        Returns
        -------
        None.

        '''
        if type(seq)==list:
            self.polynomial_seq=seq
        elif type(seq)==str:
            try:
                self.polynomial_seq=[int(c) for c in seq]
            except:
                raise ValueError('seq should be a string of integers')
        else:
            raise TypeError('seq should be a list of integers or a string of integers')
        self.mode=mode
        self.seed=seed
        
    def permutation(self,string):
        '''
        The function permutes the string using the object generator
        (i.e. 'self.polynomial_seq'). It is done few times depending on the 
        lenghts of string and generator.

        Parameters
        ----------
        string : str
            A string to be permuted

        Returns
        -------
        str
            The string after permutation.

        '''
        temp_list=list(string)
        string_len=len(string)
        for i in range(string_len // len(self.polynomial_seq)):
            move=i*len(self.polynomial_seq)
            for it,number in enumerate(self.polynomial_seq):
                temp_list[move+it],temp_list[(move+it+number)%string_len] = \
                    temp_list[(move+it+number)%string_len], temp_list[move+it]
        return ''.join(temp_list)     
        
    def polynomial_action(self,t):
        suma=0
        for i in range(len(self.polynomial_seq)):
            suma+=t**i*self.polynomial_seq[i]
        return suma %128
    
    def poly_action_on_list(self,lista):
        modified_list=list(map(self.polynomial_action,lista))
        return modified_list

    def change_string_to_int(self,text):
        intArray=[] #tablica liczb self.seed-cyfrowych 
        strNumber='' #długi napis łączący kody ascii wszystkich liter hasła
        k=self.seed #ustala ziarno podziału stringa na kawałki
        for i in range(len(text)):
            strNumber+=str(ord(text[i])*11) #*11 to make longer numbers
        for i in range(len(strNumber)//k):
            intArray.append(int(strNumber[k*i:k*(i+1)]))
        return intArray
    
    def change_int_to_string(self,tablica):
        napis=''
        '''these intervals below provide the small leter on the firs place,
        the capital letter on the second, a digit on the third and a special 
        character on the fourth place. The next positions are free'''
        intervals=[[97,122],[65,90],[48,57],[33,41]]
        for i,el in enumerate(tablica):
            if i<4:
                interval_len=intervals[i][1]-intervals[i][0]
                interval_min=intervals[i][0] 
                ascii_code=(el%interval_len)+interval_min
            else:
                ascii_code=42
                while ascii_code in [42,43]:
                    el=self.polynomial_action(el)
                    ascii_code=(el%90)+33
            napis+=chr(ascii_code)
        return napis
    
    def cipher(self,easy_password,long=False):
        '''
        

        Parameters
        ----------
        easy_password : str
            The easy-to-remember password to be transformed.
        long : bool, optional
            One can generate a longer password. It is done by concatenation of
            the short password and password obtained for double application
            of polynomial function.
            The default is False.

        Returns
        -------
        hard_password : str

        '''
        if not long:
            hard_password=self.permutation(
                self.change_int_to_string(
                        self.poly_action_on_list(
                            self.change_string_to_int(
                                self.permutation(easy_password)))))
        else:
            part1=self.poly_action_on_list(
                self.change_string_to_int(self.permutation(easy_password)))
            part2=self.poly_action_on_list(part1)
            hard_password=self.permutation(
                self.change_int_to_string(part1)+self.change_int_to_string(part2))

        return hard_password
        
if __name__=='__main__':
    seq=input('Give a 3-6 digit number (a cipher generator): ')
    s=Szyfrator(seq)
    easy_pass=input('Easy password to encrypt: ')
    hard_pass=s.cipher(easy_pass.strip(),long=False)
    print('The transformed password is: ', hard_pass)
    long_ans=input('Do you need longer password (y/n)')
    long={'y':True,'n':False}[long_ans]
    if long:
        hard_pass=s.cipher(easy_pass.strip(),long=long)
        print('The longer password is: ', hard_pass)
    else:
        print('OK')
