import scala.io.Source

object Wordcount {
  
  def main(args:Array[String]) {
  
  println(Source.fromFile("data.txt")) // returns scala.io.BufferedSource non-empty iterator instance
  
  val s1 = Source.fromFile("data.txt").mkString; //returns the file data as String
  println(s1)

  //splitting String data with white space and calculating the number of occurrence of each word in the file  
  val counts = s1.split("\\s+").groupBy(x=>x).mapValues(x=>x.length) 
  
  println(counts)
  
  println("Count of JournalDev word:"+counts("JournalDev"))
  
  }

}