class GeneratedSampleCodeBin:
    def bin_and(self, a: bool, b: bool):
        """
        >>> GeneratedSampleCodeBin().bin_and(True, True)
        True

        >>> GeneratedSampleCodeBin().bin_and(True, False)
        False

        >>> GeneratedSampleCodeBin().bin_and(False, True)
        False
        """
        if a == True:
            if b == True:
                return True
            else:
                return False
        else:
            if b == True:
                return False
            else:
                return False
    

    def bin_and_bad(self, a: bool, b: bool):
        """
        >>> GeneratedSampleCodeBin().bin_and_bad(True, True)
        True

        >>> GeneratedSampleCodeBin().bin_and_bad(True, False)
        True

        >>> GeneratedSampleCodeBin().bin_and_bad(False, True)
        True
        """
        if a == True:
            if b == True:
                return True
            else:
                return True
        else:
            if b == True:
                return True
            else:
                return False
    

    def bin_nand(self, a: bool, b: bool):
        """
        >>> GeneratedSampleCodeBin().bin_nand(True, True)
        False

        >>> GeneratedSampleCodeBin().bin_nand(True, False)
        True

        >>> GeneratedSampleCodeBin().bin_nand(False, True)
        True
        """
        if a == True:
            if b == True:
                return False
            else:
                return True
        else:
            if b == True:
                return True
            else:
                return True
    

    def bin_nor(self, a: bool, b: bool):
        """
        >>> GeneratedSampleCodeBin().bin_nor(True, True)
        False

        >>> GeneratedSampleCodeBin().bin_nor(True, False)
        False

        >>> GeneratedSampleCodeBin().bin_nor(False, True)
        False
        """
        if a == True:
            if b == True:
                return False
            else:
                return False
        else:
            if b == True:
                return False
            else:
                return True
    

    def bin_or(self, a: bool, b: bool):
        """
        >>> GeneratedSampleCodeBin().bin_or(True, True)
        True

        >>> GeneratedSampleCodeBin().bin_or(True, False)
        True

        >>> GeneratedSampleCodeBin().bin_or(False, True)
        True
        """
        if a == True:
            if b == True:
                return True
            else:
                return True
        else:
            if b == True:
                return True
            else:
                return False
    

    def bin_or_bad(self, a: bool, b: bool):
        """
        >>> GeneratedSampleCodeBin().bin_or_bad(True, True)
        False

        >>> GeneratedSampleCodeBin().bin_or_bad(True, False)
        False

        >>> GeneratedSampleCodeBin().bin_or_bad(False, True)
        False
        """
        if a == True:
            if b == True:
                return False
            else:
                return False
        else:
            if b == True:
                return False
            else:
                return True
    

    def bin_xor(self, a: bool, b: bool):
        """
        >>> GeneratedSampleCodeBin().bin_xor(True, True)
        False

        >>> GeneratedSampleCodeBin().bin_xor(True, False)
        True

        >>> GeneratedSampleCodeBin().bin_xor(False, True)
        True
        """
        if a == True:
            if b == True:
                return False
            else:
                return True
        else:
            if b == True:
                return True
            else:
                return False
    

    def mux(self, c1: bool, c2: bool, x0: bool, x1: bool, x2: bool, x3: bool):
        """
        >>> GeneratedSampleCodeBin().mux(True, True, True, True, True, True)
        True

        >>> GeneratedSampleCodeBin().mux(True, True, True, True, True, False)
        True

        >>> GeneratedSampleCodeBin().mux(True, True, True, True, False, True)
        True

        >>> GeneratedSampleCodeBin().mux(True, True, True, True, False, False)
        True

        >>> GeneratedSampleCodeBin().mux(True, True, True, False, True, True)
        True

        >>> GeneratedSampleCodeBin().mux(True, True, True, False, True, False)
        True

        >>> GeneratedSampleCodeBin().mux(True, True, True, False, False, True)
        True

        >>> GeneratedSampleCodeBin().mux(True, True, True, False, False, False)
        True

        >>> GeneratedSampleCodeBin().mux(True, True, False, True, True, True)
        False

        >>> GeneratedSampleCodeBin().mux(True, True, False, True, True, False)
        False

        >>> GeneratedSampleCodeBin().mux(True, True, False, True, False, True)
        False

        >>> GeneratedSampleCodeBin().mux(True, True, False, True, False, False)
        False

        >>> GeneratedSampleCodeBin().mux(True, True, False, False, True, True)
        False

        >>> GeneratedSampleCodeBin().mux(True, True, False, False, True, False)
        False

        >>> GeneratedSampleCodeBin().mux(True, True, False, False, False, True)
        False

        >>> GeneratedSampleCodeBin().mux(True, True, False, False, False, False)
        False

        >>> GeneratedSampleCodeBin().mux(True, False, True, True, True, True)
        True

        >>> GeneratedSampleCodeBin().mux(True, False, True, True, True, False)
        True

        >>> GeneratedSampleCodeBin().mux(True, False, True, True, False, True)
        True

        >>> GeneratedSampleCodeBin().mux(True, False, True, True, False, False)
        True

        >>> GeneratedSampleCodeBin().mux(True, False, True, False, True, True)
        False

        >>> GeneratedSampleCodeBin().mux(True, False, True, False, True, False)
        False

        >>> GeneratedSampleCodeBin().mux(True, False, True, False, False, True)
        False

        >>> GeneratedSampleCodeBin().mux(True, False, True, False, False, False)
        False

        >>> GeneratedSampleCodeBin().mux(True, False, False, True, True, True)
        True

        >>> GeneratedSampleCodeBin().mux(True, False, False, True, True, False)
        True

        >>> GeneratedSampleCodeBin().mux(True, False, False, True, False, True)
        True

        >>> GeneratedSampleCodeBin().mux(True, False, False, True, False, False)
        True

        >>> GeneratedSampleCodeBin().mux(True, False, False, False, True, True)
        False

        >>> GeneratedSampleCodeBin().mux(True, False, False, False, True, False)
        False

        >>> GeneratedSampleCodeBin().mux(True, False, False, False, False, True)
        False

        >>> GeneratedSampleCodeBin().mux(True, False, False, False, False, False)
        False

        >>> GeneratedSampleCodeBin().mux(False, True, True, True, True, True)
        True

        >>> GeneratedSampleCodeBin().mux(False, True, True, True, True, False)
        True

        >>> GeneratedSampleCodeBin().mux(False, True, True, True, False, True)
        False

        >>> GeneratedSampleCodeBin().mux(False, True, True, True, False, False)
        False

        >>> GeneratedSampleCodeBin().mux(False, True, True, False, True, True)
        True

        >>> GeneratedSampleCodeBin().mux(False, True, True, False, True, False)
        True

        >>> GeneratedSampleCodeBin().mux(False, True, True, False, False, True)
        False

        >>> GeneratedSampleCodeBin().mux(False, True, True, False, False, False)
        False

        >>> GeneratedSampleCodeBin().mux(False, True, False, True, True, True)
        True

        >>> GeneratedSampleCodeBin().mux(False, True, False, True, True, False)
        True

        >>> GeneratedSampleCodeBin().mux(False, True, False, True, False, True)
        False

        >>> GeneratedSampleCodeBin().mux(False, True, False, True, False, False)
        False

        >>> GeneratedSampleCodeBin().mux(False, True, False, False, True, True)
        True

        >>> GeneratedSampleCodeBin().mux(False, True, False, False, True, False)
        True

        >>> GeneratedSampleCodeBin().mux(False, True, False, False, False, True)
        False

        >>> GeneratedSampleCodeBin().mux(False, True, False, False, False, False)
        False

        >>> GeneratedSampleCodeBin().mux(False, False, True, True, True, True)
        True

        >>> GeneratedSampleCodeBin().mux(False, False, True, True, True, False)
        False

        >>> GeneratedSampleCodeBin().mux(False, False, True, True, False, True)
        True

        >>> GeneratedSampleCodeBin().mux(False, False, True, True, False, False)
        False

        >>> GeneratedSampleCodeBin().mux(False, False, True, False, True, True)
        True

        >>> GeneratedSampleCodeBin().mux(False, False, True, False, True, False)
        False

        >>> GeneratedSampleCodeBin().mux(False, False, True, False, False, True)
        True

        >>> GeneratedSampleCodeBin().mux(False, False, True, False, False, False)
        False

        >>> GeneratedSampleCodeBin().mux(False, False, False, True, True, True)
        True

        >>> GeneratedSampleCodeBin().mux(False, False, False, True, True, False)
        False

        >>> GeneratedSampleCodeBin().mux(False, False, False, True, False, True)
        True

        >>> GeneratedSampleCodeBin().mux(False, False, False, True, False, False)
        False

        >>> GeneratedSampleCodeBin().mux(False, False, False, False, True, True)
        True

        >>> GeneratedSampleCodeBin().mux(False, False, False, False, True, False)
        False

        >>> GeneratedSampleCodeBin().mux(False, False, False, False, False, True)
        True
        """
        if c1 == True:
            if c2 == True:
                if x0 == True:
                    if x1 == True:
                        if x2 == True:
                            if x3 == True:
                                return True
                            else:
                                return True
                        else:
                            if x3 == True:
                                return True
                            else:
                                return True
                    else:
                        if x2 == True:
                            if x3 == True:
                                return True
                            else:
                                return True
                        else:
                            if x3 == True:
                                return True
                            else:
                                return True
                else:
                    if x1 == True:
                        if x2 == True:
                            if x3 == True:
                                return False
                            else:
                                return False
                        else:
                            if x3 == True:
                                return False
                            else:
                                return False
                    else:
                        if x2 == True:
                            if x3 == True:
                                return False
                            else:
                                return False
                        else:
                            if x3 == True:
                                return False
                            else:
                                return False
            else:
                if x0 == True:
                    if x1 == True:
                        if x2 == True:
                            if x3 == True:
                                return True
                            else:
                                return True
                        else:
                            if x3 == True:
                                return True
                            else:
                                return True
                    else:
                        if x2 == True:
                            if x3 == True:
                                return False
                            else:
                                return False
                        else:
                            if x3 == True:
                                return False
                            else:
                                return False
                else:
                    if x1 == True:
                        if x2 == True:
                            if x3 == True:
                                return True
                            else:
                                return True
                        else:
                            if x3 == True:
                                return True
                            else:
                                return True
                    else:
                        if x2 == True:
                            if x3 == True:
                                return False
                            else:
                                return False
                        else:
                            if x3 == True:
                                return False
                            else:
                                return False
        else:
            if c2 == True:
                if x0 == True:
                    if x1 == True:
                        if x2 == True:
                            if x3 == True:
                                return True
                            else:
                                return True
                        else:
                            if x3 == True:
                                return False
                            else:
                                return False
                    else:
                        if x2 == True:
                            if x3 == True:
                                return True
                            else:
                                return True
                        else:
                            if x3 == True:
                                return False
                            else:
                                return False
                else:
                    if x1 == True:
                        if x2 == True:
                            if x3 == True:
                                return True
                            else:
                                return True
                        else:
                            if x3 == True:
                                return False
                            else:
                                return False
                    else:
                        if x2 == True:
                            if x3 == True:
                                return True
                            else:
                                return True
                        else:
                            if x3 == True:
                                return False
                            else:
                                return False
            else:
                if x0 == True:
                    if x1 == True:
                        if x2 == True:
                            if x3 == True:
                                return True
                            else:
                                return False
                        else:
                            if x3 == True:
                                return True
                            else:
                                return False
                    else:
                        if x2 == True:
                            if x3 == True:
                                return True
                            else:
                                return False
                        else:
                            if x3 == True:
                                return True
                            else:
                                return False
                else:
                    if x1 == True:
                        if x2 == True:
                            if x3 == True:
                                return True
                            else:
                                return False
                        else:
                            if x3 == True:
                                return True
                            else:
                                return False
                    else:
                        if x2 == True:
                            if x3 == True:
                                return True
                            else:
                                return False
                        else:
                            if x3 == True:
                                return True
                            else:
                                return False
    

