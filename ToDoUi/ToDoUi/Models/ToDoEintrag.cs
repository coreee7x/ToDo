namespace ToDoUi.Models
{
    public class ToDoEintrag
    {
        public Guid Id { get; set; }

        public string Name { get; set; }

        public string Beschreibung { get; set; }

        public Guid Liste_id { get; set; }
    }
}
