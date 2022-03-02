// Scala File handling program
import scala.io.Source
  
// Creating object 
object GeeksScala
{
    // Main method
    def main(): Unit = (args : Array[String])
    {
        // file name
        val fname = "/data/testscala.txt
  
        // creates iterable representation 
        // of the source file            
        val fSource = Source.fromFile(fname) 
        while (fSource.hasNext)
        {
            println(fSource.next)
        }
  
        // closing file
        fSource.close() 
    }
}